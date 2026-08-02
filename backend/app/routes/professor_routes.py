import secrets
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.security import exigir_professor
from backend.app.models.usuario import Usuario
from backend.app.models.turma import Turma, Disciplina
from backend.app.models.material import Material, MaterialTurmaPermissao, StatusProcessamento
from backend.app.schemas.turma import TurmaCriar, TurmaSaida
from backend.app.schemas.material import MaterialSaida, LiberarMaterialInput, MaterialTurmaPermissaoSaida
from backend.app.schemas.simulado import GerarSimuladoInput, SimuladoSaida
from backend.app.services.material_service import processar_material
from backend.app.services.simulado_service import gerar_simulado

router = APIRouter(prefix="/professor", tags=["Professor"])


# ---------- Turmas ----------

@router.post("/turmas", response_model=TurmaSaida, status_code=status.HTTP_201_CREATED)
def criar_turma(
    dados: TurmaCriar,
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    """
    A disciplina é restrita ao enum Disciplina (Historia/Geografia) já na
    validação do Pydantic — reforça o escopo do TCC desde a entrada da API.
    """
    codigo = secrets.token_urlsafe(6).upper().replace("_", "").replace("-", "")[:8]
    turma = Turma(
        nome=dados.nome,
        disciplina=dados.disciplina,
        professor_id=professor.id,  # identidade sempre do JWT, nunca do corpo da requisição
        codigo_convite=codigo,
    )
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma


@router.get("/turmas", response_model=list[TurmaSaida])
def listar_minhas_turmas(
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    return db.query(Turma).filter(Turma.professor_id == professor.id).all()


def _validar_turma_do_professor(db: Session, turma_id: int, professor_id: int) -> Turma:
    turma = (
        db.query(Turma)
        .filter(Turma.id == turma_id, Turma.professor_id == professor_id)
        .first()
    )
    if turma is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Turma não encontrada ou não pertence a este professor.",
        )
    return turma


# ---------- Materiais ----------

@router.post("/materiais", response_model=MaterialSaida, status_code=status.HTTP_201_CREATED)
def enviar_material(
    background_tasks: BackgroundTasks,
    titulo: str = Form(...),
    disciplina: Disciplina = Form(...),
    arquivo: UploadFile = File(...),
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    destino = upload_dir / f"{secrets.token_hex(8)}_{arquivo.filename}"
    with destino.open("wb") as f:
        shutil.copyfileobj(arquivo.file, f)

    material = Material(
        titulo=titulo,
        nome_arquivo=arquivo.filename,
        caminho_arquivo=str(destino),
        disciplina=disciplina.value,
        professor_id=professor.id,
        status_processamento=StatusProcessamento.PENDENTE,
    )
    db.add(material)
    db.commit()
    db.refresh(material)

    # Processamento em background — ver nota de arquitetura em material_service.py
    background_tasks.add_task(processar_material, material.id, db)

    return material


@router.get("/materiais", response_model=list[MaterialSaida])
def listar_meus_materiais(
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    return db.query(Material).filter(Material.professor_id == professor.id).all()


@router.post(
    "/materiais/{material_id}/liberar",
    response_model=list[MaterialTurmaPermissaoSaida],
    status_code=status.HTTP_201_CREATED,
)
def liberar_material_para_turmas(
    material_id: int,
    dados: LiberarMaterialInput,
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    """
    Cria os registros de MaterialTurmaPermissao — o único lugar do sistema
    onde se decide QUANDO cada turma pode acessar QUAL material.
    """
    material = (
        db.query(Material)
        .filter(Material.id == material_id, Material.professor_id == professor.id)
        .first()
    )
    if material is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado.")

    if material.status_processamento != StatusProcessamento.CONCLUIDO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Material ainda não está pronto (status: {material.status_processamento.value}).",
        )

    permissoes_criadas = []
    for turma_id in dados.turma_ids:
        _validar_turma_do_professor(db, turma_id, professor.id)  # garante posse da turma

        permissao = MaterialTurmaPermissao(
            material_id=material.id,
            turma_id=turma_id,
            data_liberacao=dados.data_liberacao,
        )
        db.add(permissao)
        permissoes_criadas.append(permissao)

    db.commit()
    for p in permissoes_criadas:
        db.refresh(p)
    return permissoes_criadas


# ---------- Simulados ----------

@router.post("/simulados", response_model=SimuladoSaida, status_code=status.HTTP_201_CREATED)
def criar_simulado(
    dados: GerarSimuladoInput,
    professor: Usuario = Depends(exigir_professor),
    db: Session = Depends(get_db),
):
    _validar_turma_do_professor(db, dados.turma_id, professor.id)

    try:
        simulado = gerar_simulado(
            db=db,
            turma_id=dados.turma_id,
            titulo=dados.titulo,
            numero_questoes=dados.numero_questoes,
            criado_por_id=professor.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    return simulado
