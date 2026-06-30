from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Utilizamos importações relativas (com os dois pontos "..") 
# para resolver definitivamente o erro de "unknown location".
from ..database import get_db
from ..models import Turma
from ..schemas import TurmaCreate

router = APIRouter()

@router.post("/turmas/")
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    # Recebe os dados validados pelo schema e guarda na base de dados
    nova_turma = Turma(nome=turma.nome, ano_escolar=turma.ano_escolar)
    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    return nova_turma