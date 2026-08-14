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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.app.core.database import SessionLocal
from backend.app.models.material import Material, StatusProcessamento
from backend.app.services.gemini_client import gemini_client
from backend.app.services.rag_service import _collection

logger = logging.getLogger(__name__)

TAMANHO_CHUNK = 1000  # caracteres
SOBREPOSICAO_CHUNK = 150

# Nº de chamadas de embedding em paralelo. Cada chamada é I/O-bound (rede), então
# threads ajudam mesmo com o GIL. Limitado ao nº de chaves Gemini disponíveis
# para não estourar a quota de uma única chave com concorrência excessiva.
MAX_WORKERS_EMBEDDING = max(4, len(gemini_client._chaves) * 4)


def extrair_texto_pdf(caminho_arquivo: str) -> str:
    """
    Extrai o texto de um PDF. Só material com texto de fato extraível é aceito
    aqui — PDFs criptografados ou corrompidos viram um erro claro para o
    professor, em vez de deixar o pypdf estourar uma exceção genérica.
    """
    try:
        leitor = PdfReader(caminho_arquivo)
    except PdfReadError as e:
        raise ValueError(f"Arquivo PDF corrompido ou inválido: {e}") from e

    if leitor.is_encrypted:
        raise ValueError("O PDF está protegido por senha e não pode ser lido.")

    return "\n".join(pagina.extract_text() or "" for pagina in leitor.pages)


def dividir_em_chunks(texto: str, tamanho: int = TAMANHO_CHUNK, sobreposicao: int = SOBREPOSICAO_CHUNK) -> list[str]:
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao
    return [c.strip() for c in chunks if c.strip()]


def processar_material(material_id: int) -> None:
    """
    Função executada em background (BackgroundTasks) após o upload.
    Usa uma sessão própria para o trabalho assíncrono e evita reutilizar a
    sessão HTTP da requisição que já foi fechada.
    """
    db = SessionLocal()
    try:
        material = db.query(Material).filter(Material.id == material_id).first()
        if material is None:
            logger.error("Material %s não encontrado para processamento.", material_id)
            return

        material.status_processamento = StatusProcessamento.PROCESSANDO
        db.commit()

        try:
            extensao = Path(material.caminho_arquivo).suffix.lower()
            if extensao != ".pdf":
                # Escopo do TCC: apenas PDF. A rota de upload já rejeita outras
                # extensões antes de chegar aqui; este é só um cinto de segurança.
                raise ValueError(f"Tipo de arquivo não suportado: {extensao or 'desconhecido'}. Envie um PDF.")

            texto = extrair_texto_pdf(material.caminho_arquivo)

            if not texto.strip():
                raise ValueError(
                    "Não foi possível extrair texto do PDF — provavelmente é um documento "
                    "escaneado (imagem) sem camada de texto reconhecível."
                )

            chunks = dividir_em_chunks(texto)

            # As chamadas de embedding são feitas em paralelo (I/O de rede) em vez de
            # sequencialmente: era o principal gargalo de performance do pipeline —
            # um documento com muitos chunks pagava uma latência de rede inteira, uma
            # de cada vez, quando poderiam ser concorrentes.
            with ThreadPoolExecutor(max_workers=MAX_WORKERS_EMBEDDING) as executor:
                embeddings = list(executor.map(gemini_client.gerar_embedding, chunks))

            ids = [f"material-{material.id}-chunk-{i}" for i in range(len(chunks))]
            metadados = [{"material_id": material.id, "disciplina": material.disciplina} for _ in chunks]

            if ids:
                _collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadados)

            material.status_processamento = StatusProcessamento.CONCLUIDO
            material.mensagem_erro = None
            db.commit()
            logger.info("Material %s processado com sucesso (%d chunks).", material_id, len(chunks))

        except Exception as e:
            logger.exception("Erro ao processar material %s", material_id)
            material.status_processamento = StatusProcessamento.ERRO
            material.mensagem_erro = str(e)
            db.commit()
    finally:
        db.close()


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
