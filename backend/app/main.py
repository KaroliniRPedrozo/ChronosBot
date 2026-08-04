import logging

from backend.app.routes import aluno_routes, auth_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app import models  # noqa: F401 - garante que todos os models sejam registrados no Base.metadata
from backend.app.routes import professor_routes
from backend.seed_test_data import reparar_esquema_antigo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ChronosBot API",
    description=(
        "API do ChronosBot — plataforma de tutoria educacional com IA para "
        "as disciplinas de História e Geografia. TCC desenvolvido por Karolini R. Pedrozo."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(professor_routes.router)
app.include_router(aluno_routes.router)


@app.on_event("startup")
def criar_tabelas():
    """
    Cria as tabelas automaticamente no startup — adequado para o escopo do TCC.
    Em produção, o recomendado seria usar Alembic para migrações versionadas.
    """
    Base.metadata.create_all(bind=engine)
    reparar_esquema_antigo()
    logger.info("Tabelas verificadas/criadas e esquema legado reparado com sucesso.")


@app.get("/", tags=["Status"])
def raiz():
    return {"status": "ok", "servico": "ChronosBot API"}


@app.get("/health", tags=["Status"])
def health_check():
    return {"status": "healthy"}
