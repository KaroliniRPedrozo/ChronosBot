import enum
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint, func
)
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Disciplina(str, enum.Enum):
    HISTORIA = "Historia"
    GEOGRAFIA = "Geografia"


class Turma(Base):
    """
    Uma turma é sempre vinculada a UMA disciplina (Historia ou Geografia),
    conforme o escopo do TCC. Essa restrição é validada em routes_professor.py
    e reforçada nas consultas de rag.py.
    """
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    disciplina = Column(Enum(Disciplina, native_enum=False), nullable=False)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    codigo_convite = Column(String(20), unique=True, nullable=False, index=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    professor = relationship("Usuario", back_populates="turmas_lecionadas", foreign_keys=[professor_id])
    matriculas = relationship("Matricula", back_populates="turma", cascade="all, delete-orphan")
    materiais_liberados = relationship("MaterialTurmaPermissao", back_populates="turma")
    sessoes_chat = relationship("SessaoChat", back_populates="turma")
    simulados = relationship("Simulado", back_populates="turma")


class Matricula(Base):
    """Vínculo N:N entre aluno e turma."""
    __tablename__ = "matriculas"
    __table_args__ = (UniqueConstraint("aluno_id", "turma_id", name="uq_aluno_turma"),)

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    matriculado_em = Column(DateTime(timezone=True), server_default=func.now())

    aluno = relationship("Usuario", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")
