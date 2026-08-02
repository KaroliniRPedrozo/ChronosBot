"""
Geração de simulados (quizzes) via Gemini.

Estratégia: pedir saída em JSON estrito, validar com Pydantic
(SimuladoGeradoIA) e, se a validação falhar, reenviar ao modelo o erro
específico pedindo correção — até um número máximo de tentativas.
"""
import json
import logging

from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.app.models.material import Material
from backend.app.models.simulado import Simulado, Questao
from backend.app.schemas.simulado import SimuladoGeradoIA
from backend.app.services.gemini_client import gemini_client
from backend.app.services.rag_service import obter_materiais_permitidos, _collection

logger = logging.getLogger(__name__)

MAX_TENTATIVAS = 3

SYSTEM_PROMPT_SIMULADO = """\
Você cria simulados de múltipla escolha para alunos de ensino médio, com base \
apenas no contexto de materiais fornecido. Responda ESTRITAMENTE em JSON, no \
seguinte formato, sem nenhum texto adicional antes ou depois:

{
  "questoes": [
    {
      "enunciado": "...",
      "alternativas": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "resposta_correta": "A",
      "explicacao": "..."
    }
  ]
}
"""


def _obter_contexto_para_turma(db: Session, turma_id: int, limite_chunks: int = 20) -> str:
    """Reaproveita a mesma restrição de acesso do rag_service: só materiais liberados."""
    material_ids = obter_materiais_permitidos(db, turma_id)
    if not material_ids:
        raise ValueError("Nenhum material liberado para esta turma ainda.")

    resultados = _collection.get(
        where={"material_id": {"$in": material_ids}},
        limit=limite_chunks,
    )
    documentos = resultados.get("documents", [])
    if not documentos:
        raise ValueError("Materiais liberados ainda não foram indexados (processamento pendente).")
    return "\n\n---\n\n".join(documentos)


def gerar_simulado(
    db: Session, turma_id: int, titulo: str, numero_questoes: int, criado_por_id: int
) -> Simulado:
    contexto = _obter_contexto_para_turma(db, turma_id)

    prompt = (
        f"Contexto:\n{contexto}\n\n"
        f"Gere exatamente {numero_questoes} questões de múltipla escolha "
        f"baseadas neste contexto, seguindo o formato JSON especificado."
    )

    erro_anterior = None
    simulado_validado = None

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        prompt_atual = prompt
        if erro_anterior:
            prompt_atual += (
                f"\n\nATENÇÃO: a resposta anterior falhou na validação com o erro: "
                f"'{erro_anterior}'. Corrija e responda novamente em JSON válido."
            )

        bruto = gemini_client.gerar_texto(
            prompt_atual, system_instruction=SYSTEM_PROMPT_SIMULADO, json_mode=True
        )

        try:
            dados = json.loads(bruto)
            simulado_validado = SimuladoGeradoIA(**dados)
            break
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning("Tentativa %d de gerar simulado falhou: %s", tentativa, e)
            erro_anterior = str(e)
            continue

    if simulado_validado is None:
        raise RuntimeError(
            f"Não foi possível gerar um simulado válido após {MAX_TENTATIVAS} tentativas."
        )

    simulado = Simulado(titulo=titulo, turma_id=turma_id, criado_por_id=criado_por_id)
    db.add(simulado)
    db.flush()  # obtém simulado.id sem commitar ainda

    for i, q in enumerate(simulado_validado.questoes):
        db.add(
            Questao(
                simulado_id=simulado.id,
                ordem=i + 1,
                enunciado=q.enunciado,
                alternativas=q.alternativas,
                resposta_correta=q.resposta_correta,
                explicacao=q.explicacao,
            )
        )

    db.commit()
    db.refresh(simulado)
    return simulado
