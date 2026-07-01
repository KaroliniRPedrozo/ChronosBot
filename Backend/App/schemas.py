from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# ---------- Turma ----------
class TurmaCreate(BaseModel):
    nome: str
    ano_escolar: str


class TurmaOut(BaseModel):
    id: int
    nome: str
    ano_escolar: str

    class Config:
        from_attributes = True  # pydantic v2 (use orm_mode = True se for pydantic v1)


# ---------- Professor ----------
class ProfessorCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class ProfessorOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True


# ---------- Aluno ----------
class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    turma_id: int


class AlunoOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    turma_id: int

    class Config:
        from_attributes = True


# ---------- Material ----------
class MaterialCreate(BaseModel):
    titulo: str
    turma_id: int
    data_liberacao: date


class MaterialOut(BaseModel):
    id: int
    titulo: str
    nome_arquivo: str
    turma_id: int
    data_liberacao: date
    processado: bool

    class Config:
        from_attributes = True