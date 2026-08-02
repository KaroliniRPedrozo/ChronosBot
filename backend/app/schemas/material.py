from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.material import StatusProcessamento


class MaterialSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    nome_arquivo: str
    disciplina: str
    status_processamento: StatusProcessamento
    mensagem_erro: Optional[str] = None
    criado_em: datetime


class LiberarMaterialInput(BaseModel):
    """Payload para liberar um material já existente para uma ou mais turmas."""
    turma_ids: List[int] = Field(min_length=1)
    data_liberacao: datetime


class MaterialTurmaPermissaoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    material_id: int
    turma_id: int
    data_liberacao: datetime
