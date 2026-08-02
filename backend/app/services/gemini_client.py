"""
Cliente wrapper para a API do Google Gemini.

Implementa rotação de chaves (round-robin) para contornar os limites de
quota do free tier — se uma chave atingir o limite de requisições, a
próxima chamada tenta a chave seguinte da lista.
"""
import itertools
import logging
from typing import Optional

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClientRotativo:
    def __init__(self):
        chaves = settings.gemini_keys_list
        if not chaves:
            raise RuntimeError(
                "Nenhuma GEMINI_API_KEY configurada. Defina GEMINI_API_KEY ou GEMINI_API_KEYS no .env."
            )
        self._chaves = chaves
        self._ciclo = itertools.cycle(range(len(chaves)))

    def _proximo_cliente(self) -> genai.Client:
        idx = next(self._ciclo)
        return genai.Client(api_key=self._chaves[idx])

    def gerar_texto(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        temperatura: float = 0.4,
    ) -> str:
        """
        Gera texto com o modelo configurado (gemini-1.5-flash), tentando
        cada chave disponível em caso de erro de quota (HTTP 429).
        """
        ultimo_erro = None
        for _ in range(len(self._chaves)):
            cliente = self._proximo_cliente()
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperatura,
                    response_mime_type="application/json" if json_mode else "text/plain",
                )
                resposta = cliente.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                    config=config,
                )
                return resposta.text
            except ClientError as e:
                ultimo_erro = e
                if getattr(e, "code", None) == 429:
                    logger.warning("Chave Gemini atingiu quota, tentando a próxima.")
                    continue
                raise
        raise RuntimeError(f"Todas as chaves Gemini falharam. Último erro: {ultimo_erro}")

    def gerar_embedding(self, texto: str) -> list[float]:
        """Gera embedding de um texto usando models/text-embedding-004."""
        ultimo_erro = None
        for _ in range(len(self._chaves)):
            cliente = self._proximo_cliente()
            try:
                resposta = cliente.models.embed_content(
                    model=settings.GEMINI_EMBEDDING_MODEL,
                    contents=texto,
                )
                return resposta.embeddings[0].values
            except ClientError as e:
                ultimo_erro = e
                if getattr(e, "code", None) == 429:
                    continue
                raise
        raise RuntimeError(f"Todas as chaves Gemini falharam ao gerar embedding: {ultimo_erro}")


gemini_client = GeminiClientRotativo()
