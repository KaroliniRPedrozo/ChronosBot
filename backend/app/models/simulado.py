from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float, func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Simulado(Base):
    """Um simulado (quiz) gerado por IA a partir dos materiais liberados para a turma."""
    __tablename__ = "simulados"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    criado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    turma = relationship("Turma", back_populates="simulados")
    questoes = relationship(
        "Questao", back_populates="simulado", cascade="all, delete-orphan",
        order_by="Questao.ordem",
    )
    tentativas = relationship("TentativaSimulado", back_populates="simulado")


class Questao(Base):
    """
    Questão de múltipla escolha, gerada pelo Gemini com saída JSON estruturada
    e validação via Pydantic (ver services/simulado_service.py).
    """
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    ordem = Column(Integer, nullable=False)
    enunciado = Column(Text, nullable=False)
    alternativas = Column(JSON, nullable=False)  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    resposta_correta = Column(String(1), nullable=False)  # "A", "B", "C" ou "D"
    explicacao = Column(Text, nullable=True)

    simulado = relationship("Simulado", back_populates="questoes")


class TentativaSimulado(Base):
    """Registro de uma tentativa de resolução do simulado por um aluno."""
    __tablename__ = "tentativas_simulado"

    id = Column(Integer, primary_key=True, index=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    respostas = Column(JSON, nullable=False)  # {"questao_id": "A", ...}
    nota = Column(Float, nullable=False)
    finalizado_em = Column(DateTime(timezone=True), server_default=func.now())

    simulado = relationship("Simulado", back_populates="tentativas")
    aluno = relationship("Usuario", back_populates="tentativas_simulado")
