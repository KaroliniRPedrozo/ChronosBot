from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.turma import Disciplina


class TurmaCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    disciplina: Disciplina


class TurmaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    disciplina: Disciplina
    codigo_convite: str
    criado_em: datetime


class TurmaEntrar(BaseModel):
    """Usado pelo aluno para entrar em uma turma via código de convite."""
    codigo_convite: str = Field(min_length=4, max_length=20)


class MatriculaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    turma_id: int
    aluno_id: int
    matriculado_em: datetime
