import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class SessaoChat(Base):
    """
    Cada sessão agrupa uma conversa entre um aluno e o tutor de IA,
    dentro do escopo de uma turma. Serve como trilha de auditoria
    (relevante para conformidade com a LGPD).
    """
    __tablename__ = "sessoes_chat"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    iniciada_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizada_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    aluno = relationship("Usuario", back_populates="sessoes_chat")
    turma = relationship("Turma", back_populates="sessoes_chat")
    mensagens = relationship(
        "Mensagem", back_populates="sessao", cascade="all, delete-orphan",
        order_by="Mensagem.criado_em",
    )


class RemetenteMensagem(str, enum.Enum):
    ALUNO = "aluno"
    ASSISTENTE = "assistente"


class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(Integer, ForeignKey("sessoes_chat.id"), nullable=False)
    remetente = Column(Enum(RemetenteMensagem), nullable=False)
    conteudo = Column(Text, nullable=False)
    # IDs dos materiais usados como contexto nesta resposta (auditoria/transparência)
    materiais_utilizados = Column(String(500), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    sessao = relationship("SessaoChat", back_populates="mensagens")
