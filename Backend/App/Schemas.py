from pydantic import BaseModel
from typing import Optional

class TurmaBase(BaseModel):
    nome: str
    ano_escolar: str

class TurmaCreate(TurmaBase):
    pass

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    role: str
    turma_id: Optional[int] = None