import enum
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, ForeignKey, Index, Text, func
)
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class StatusProcessamento(str, enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    CONCLUIDO = "concluido"
    ERRO = "erro"


class Material(Base):
    """
    Representa um documento enviado pelo professor (PDF, texto etc.).
    A existência do material é independente de sua liberação para turmas
    específicas — isso é resolvido em MaterialTurmaPermissao.
    """
    __tablename__ = "materiais"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_arquivo = Column(String(500), nullable=False)
    disciplina = Column(String(50), nullable=False)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status_processamento = Column(
        Enum(StatusProcessamento), default=StatusProcessamento.PENDENTE, nullable=False
    )
    mensagem_erro = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    professor = relationship("Usuario")
    permissoes = relationship(
        "MaterialTurmaPermissao", back_populates="material", cascade="all, delete-orphan"
    )


class MaterialTurmaPermissao(Base):
    """
    ARQUITETURA CENTRAL: esta tabela é o ponto único de decisão sobre o que
    cada turma pode acessar, e a partir de quando (data_liberacao).

    O RAG NUNCA faz busca vetorial diretamente sobre todos os materiais.
    Fluxo obrigatório (rag.py):
      1) Consulta relacional aqui, filtrando por turma_id E data_liberacao <= now()
         -> obtém a lista de material_id permitidos
      2) SÓ ENTÃO faz busca vetorial no ChromaDB, restrita a esses material_id

    Isso garante que o LLM nunca "veja" conteúdo fora do escopo — o controle
    de acesso acontece na camada de dados, não via instrução de prompt.
    """
    __tablename__ = "material_turma_permissao"
    __table_args__ = (
        Index("ix_turma_data_liberacao", "turma_id", "data_liberacao"),
    )

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    data_liberacao = Column(DateTime(timezone=True), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    material = relationship("Material", back_populates="permissoes")
    turma = relationship("Turma", back_populates="materiais_liberados")
