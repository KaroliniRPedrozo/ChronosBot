from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importações relativas com os nomes em minúsculas
from ..database import get_db
from ..models import Turma
from ..schemas import TurmaCreate

router = APIRouter()

@router.post("/turmas/")
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    nova_turma = Turma(nome=turma.nome, ano_escolar=turma.ano_escolar)
    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    return nova_turma