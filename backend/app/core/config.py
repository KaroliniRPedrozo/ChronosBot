"""
Configurações centrais do ChronosBot.
Carrega variáveis de ambiente e expõe um objeto `settings` único para toda a aplicação.
"""
import ast
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Banco de dados ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/chronosbot",
    )

    # --- Autenticação / JWT ---
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))  # 8h

    # --- Google Gemini ---
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"
    GEMINI_EMBEDDING_DIMENSIONS: int = 768  # mantém compatibilidade com chunks já indexados

    # Rotação de chaves (free tier) - lista separada por vírgula em GEMINI_API_KEYS
    GEMINI_API_KEYS: str = os.getenv("GEMINI_API_KEYS", "")

    # --- ChromaDB ---
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
    CHROMA_COLLECTION_NAME: str = "chronosbot_materiais"

    # --- Disciplinas permitidas (escopo do TCC) ---
    DISCIPLINAS_PERMITIDAS: list[str] = ["Historia", "Geografia"]

    # --- Upload de materiais ---
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE_MB: int = 25

    # --- CORS ---
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        case_sensitive = True

    @property
    def frontend_origins(self) -> list[str]:
        """Retorna a lista de origens permitidas para CORS a partir de FRONTEND_URL."""
        raw = self.FRONTEND_URL.strip()
        if not raw:
            return []
        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, (list, tuple)):
                    return [str(url).strip() for url in parsed if url]
            except Exception:
                pass
        return [url.strip() for url in raw.split(",") if url.strip()]

    @property
    def gemini_keys_list(self) -> list[str]:
        """Retorna lista de chaves Gemini para rotação (fallback para GEMINI_API_KEY única)."""
        # Prioridade: GEMINI_API_KEYS (coma-separated ou lista Python-like) -> GEMINI_API_KEY_N env vars -> single GEMINI_API_KEY
        if self.GEMINI_API_KEYS:
            raw = self.GEMINI_API_KEYS.strip()
            if raw.startswith("[") and raw.endswith("]"):
                try:
                    parsed = ast.literal_eval(raw)
                    if isinstance(parsed, (list, tuple)):
                        return [str(k).strip() for k in parsed if k]
                except Exception:
                    pass
            return [k.strip() for k in raw.split(",") if k.strip()]

        # Detect environment variables like GEMINI_API_KEY_1, GEMINI_API_KEY_2, ...
        env_keys = []
        for name, val in os.environ.items():
            if name.upper().startswith("GEMINI_API_KEY_") and val:
                env_keys.append((name, val))
        if env_keys:
            try:
                env_keys = [v for _, v in sorted(
                    ((int(k.split("_")[-1]), v) for k, v in env_keys),
                    key=lambda x: x[0]
                )]
                return [v for _, v in env_keys]
            except Exception:
                return [v for _, v in env_keys]

        return [self.GEMINI_API_KEY] if self.GEMINI_API_KEY else []


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
