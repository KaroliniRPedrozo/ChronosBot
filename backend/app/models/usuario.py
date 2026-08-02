import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class PapelUsuario(str, enum.Enum):
    PROFESSOR = "professor"
    ALUNO = "aluno"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    papel = Column(Enum(PapelUsuario, native_enum=False), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    turmas_lecionadas = relationship(
        "Turma", back_populates="professor", foreign_keys="Turma.professor_id"
    )
    matriculas = relationship("Matricula", back_populates="aluno")
    sessoes_chat = relationship("SessaoChat", back_populates="aluno")
    tentativas_simulado = relationship("TentativaSimulado", back_populates="aluno")
