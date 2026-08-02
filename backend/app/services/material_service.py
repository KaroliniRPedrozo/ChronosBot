"""
Serviço de processamento de materiais enviados pelo professor.

NOTA DE ARQUITETURA (questão em aberto no projeto):
  Atualmente o processamento roda em BackgroundTasks do FastAPI (assíncrono
  em relação à requisição HTTP, mas ainda em processo único). Isso evita que
  o professor espere o upload travar a resposta, mas ainda compartilha os
  recursos do servidor web.

  Para produção/escala, a recomendação é migrar para uma fila real
  (Celery + Redis, ou RQ) — ver docstring no final do arquivo.
"""
import logging
from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.material import Material, StatusProcessamento
from backend.app.services.gemini_client import gemini_client
from backend.app.services.rag_service import _collection

logger = logging.getLogger(__name__)

TAMANHO_CHUNK = 1000  # caracteres
SOBREPOSICAO_CHUNK = 150


def extrair_texto_pdf(caminho_arquivo: str) -> str:
    leitor = PdfReader(caminho_arquivo)
    return "\n".join(pagina.extract_text() or "" for pagina in leitor.pages)


def dividir_em_chunks(texto: str, tamanho: int = TAMANHO_CHUNK, sobreposicao: int = SOBREPOSICAO_CHUNK) -> list[str]:
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao
    return [c.strip() for c in chunks if c.strip()]


def processar_material(material_id: int, db: Session) -> None:
    """
    Função executada em background (BackgroundTasks) após o upload.
    Extrai texto, divide em chunks, gera embeddings e indexa no ChromaDB
    com metadado material_id — essencial para o filtro `where` do rag_service.
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if material is None:
        logger.error("Material %s não encontrado para processamento.", material_id)
        return

    material.status_processamento = StatusProcessamento.PROCESSANDO
    db.commit()

    try:
        extensao = Path(material.caminho_arquivo).suffix.lower()
        if extensao == ".pdf":
            texto = extrair_texto_pdf(material.caminho_arquivo)
        else:
            texto = Path(material.caminho_arquivo).read_text(encoding="utf-8", errors="ignore")

        if not texto.strip():
            raise ValueError("Não foi possível extrair texto do arquivo (arquivo vazio ou ilegível).")

        chunks = dividir_em_chunks(texto)

        ids, embeddings, documentos, metadados = [], [], [], []
        for i, chunk in enumerate(chunks):
            embedding = gemini_client.gerar_embedding(chunk)
            ids.append(f"material-{material.id}-chunk-{i}")
            embeddings.append(embedding)
            documentos.append(chunk)
            metadados.append({"material_id": material.id, "disciplina": material.disciplina})

        if ids:
            _collection.add(ids=ids, embeddings=embeddings, documents=documentos, metadatas=metadados)

        material.status_processamento = StatusProcessamento.CONCLUIDO
        material.mensagem_erro = None
        db.commit()
        logger.info("Material %s processado com sucesso (%d chunks).", material_id, len(chunks))

    except Exception as e:
        logger.exception("Erro ao processar material %s", material_id)
        material.status_processamento = StatusProcessamento.ERRO
        material.mensagem_erro = str(e)
        db.commit()


"""
DECISÃO EM ABERTO — processamento síncrono vs. assíncrono/background:

Opção atual (implementada): FastAPI BackgroundTasks.
  Prós: simples, sem infraestrutura extra, suficiente para o volume de um TCC.
  Contras: ainda compete por CPU/IO com as requisições da API; não sobrevive
  a um restart do servidor a meio do processamento; sem retry automático.

Alternativa para produção: fila dedicada (Celery+Redis ou RQ).
  Prós: resiliente a restarts, permite retry e monitoramento, desacopla do
  processo web.
  Contras: mais infraestrutura para configurar em um ambiente de Codespaces.

Recomendação para o escopo do TCC: manter BackgroundTasks e documentar a
fila como "trabalho futuro" na monografia — é uma decisão de engenharia
perfeitamente defensável para o tamanho do projeto.
"""
