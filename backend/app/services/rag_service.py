"""
Serviço de Retrieval-Augmented Generation.

PRINCÍPIO ARQUITETURAL (não negociável):
  O controle de acesso acontece na camada de dados, não via instrução de prompt.
  O LLM NUNCA recebe conteúdo de materiais que o aluno não deveria ver.

Fluxo obrigatório de retrieval em duas etapas:
  1) Consulta RELACIONAL no PostgreSQL: dado turma_id, obtém a lista de
     material_id cuja data_liberacao já passou (MaterialTurmaPermissao).
  2) Busca VETORIAL no ChromaDB, restrita (filtro `where`) a esses material_id.

Nunca fazer o passo 2 antes do passo 1, e nunca pular o passo 1.
"""
import logging
from datetime import datetime, timezone
from typing import List, Tuple

import chromadb
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.material import MaterialTurmaPermissao
from backend.app.services.gemini_client import gemini_client

logger = logging.getLogger(__name__)

_chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
_collection = _chroma_client.get_or_create_collection(name=settings.CHROMA_COLLECTION_NAME)


def obter_materiais_permitidos(db: Session, turma_id: int) -> List[int]:
    """
    ETAPA 1 — consulta relacional.
    Retorna os IDs de materiais liberados para a turma até o momento atual.
    """
    agora = datetime.now(timezone.utc)
    permissoes = (
        db.query(MaterialTurmaPermissao.material_id)
        .filter(
            MaterialTurmaPermissao.turma_id == turma_id,
            MaterialTurmaPermissao.data_liberacao <= agora,
        )
        .distinct()
        .all()
    )
    return [p.material_id for p in permissoes]


def buscar_trechos_relevantes(
    pergunta: str, material_ids_permitidos: List[int], top_k: int = 5
) -> List[Tuple[str, int]]:
    """
    ETAPA 2 — busca vetorial, restrita aos material_ids já autorizados.
    Retorna lista de (trecho_texto, material_id).

    Se material_ids_permitidos estiver vazio, retorna lista vazia SEM
    consultar o ChromaDB — não há necessidade de buscar em um universo nulo,
    e isso evita qualquer chance de vazamento por erro de filtro.
    """
    if not material_ids_permitidos:
        return []

    embedding_pergunta = gemini_client.gerar_embedding(pergunta)

    resultados = _collection.query(
        query_embeddings=[embedding_pergunta],
        n_results=top_k,
        where={"material_id": {"$in": material_ids_permitidos}},
    )

    trechos = []
    documentos = resultados.get("documents", [[]])[0]
    metadados = resultados.get("metadatas", [[]])[0]
    for doc, meta in zip(documentos, metadados):
        trechos.append((doc, meta["material_id"]))
    return trechos


SYSTEM_PROMPT_TUTOR = """\
Você é um tutor educacional especializado em História e Geografia, parte da \
plataforma ChronosBot. Responda SOMENTE com base nos trechos de contexto \
fornecidos abaixo. Se a resposta não estiver no contexto, diga claramente que \
o material disponível não cobre esse tópico — não invente informações.
Responda em português, de forma didática e adequada ao nível de ensino médio.
"""


def responder_pergunta_aluno(
    db: Session, turma_id: int, pergunta: str
) -> Tuple[str, List[int]]:
    """
    Orquestra o fluxo completo: obtém materiais permitidos, busca trechos
    relevantes, e chama o Gemini com o contexto restrito.
    Retorna (resposta_texto, lista_material_ids_usados).
    """
    material_ids_permitidos = obter_materiais_permitidos(db, turma_id)

    if not material_ids_permitidos:
        return (
            "Ainda não há materiais liberados para esta turma. "
            "Fale com seu professor para saber quando o conteúdo estará disponível.",
            [],
        )

    trechos = buscar_trechos_relevantes(pergunta, material_ids_permitidos)

    if not trechos:
        return (
            "Não encontrei informações sobre isso nos materiais liberados até o momento.",
            [],
        )

    contexto = "\n\n---\n\n".join(t[0] for t in trechos)
    material_ids_usados = sorted(set(t[1] for t in trechos))

    prompt = f"Contexto:\n{contexto}\n\nPergunta do aluno: {pergunta}"
    resposta = gemini_client.gerar_texto(prompt, system_instruction=SYSTEM_PROMPT_TUTOR)

    return resposta, material_ids_usados
