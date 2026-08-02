from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.chat import RemetenteMensagem


class ChatPerguntaInput(BaseModel):
    turma_id: int
    sessao_id: Optional[int] = None  # se None, cria nova sessão
    pergunta: str = Field(min_length=1, max_length=2000)


class MensagemSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    remetente: RemetenteMensagem
    conteudo: str
    criado_em: datetime


class ChatRespostaSaida(BaseModel):
    sessao_id: int
    resposta: str
    materiais_utilizados: List[int] = []


class SessaoChatSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    turma_id: int
    iniciada_em: datetime
    mensagens: List[MensagemSaida] = []
