from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database import Base
import datetime


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)

    turmas = relationship("Turma", back_populates="professor")


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)          # ex: "6 Ano A"
    ano_escolar = Column(String, nullable=False)    # ex: "6 Ano"
    professor_id = Column(Integer, ForeignKey("professores.id"))

    professor = relationship("Professor", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma")
    materiais = relationship("Material", back_populates="turma")


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)

    turma = relationship("Turma", back_populates="alunos")


class Material(Base):
    __tablename__ = "materiais"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    nome_arquivo = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False)   # path no disco/storage
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    data_liberacao = Column(Date, nullable=False)       # regra de ouro do RAG
    processado = Column(Boolean, default=False)         # já foi feito embedding?
    criado_em = Column(DateTime, default=datetime.datetime.utcnow)

    turma = relationship("Turma", back_populates="materiais")