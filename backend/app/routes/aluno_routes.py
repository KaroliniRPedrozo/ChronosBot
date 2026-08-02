from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import exigir_aluno
from backend.app.models.usuario import Usuario
from backend.app.models.turma import Turma, Matricula
from backend.app.models.chat import SessaoChat, Mensagem, RemetenteMensagem
from backend.app.models.simulado import Simulado, Questao, TentativaSimulado
from backend.app.schemas.turma import TurmaEntrar, TurmaSaida, MatriculaSaida
from backend.app.schemas.chat import ChatPerguntaInput, ChatRespostaSaida, SessaoChatSaida
from backend.app.schemas.simulado import SimuladoSaida, ResponderSimuladoInput, TentativaSaida, QuestaoComGabaritoSaida
from backend.app.services.rag_service import responder_pergunta_aluno

router = APIRouter(prefix="/aluno", tags=["Aluno"])


# ---------- Turmas ----------

@router.post("/turmas/entrar", response_model=MatriculaSaida, status_code=status.HTTP_201_CREATED)
def entrar_em_turma(
    dados: TurmaEntrar,
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    turma = db.query(Turma).filter(Turma.codigo_convite == dados.codigo_convite).first()
    if turma is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Código de convite inválido.")

    ja_matriculado = (
        db.query(Matricula)
        .filter(Matricula.aluno_id == aluno.id, Matricula.turma_id == turma.id)
        .first()
    )
    if ja_matriculado:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Você já está matriculado nesta turma.")

    matricula = Matricula(aluno_id=aluno.id, turma_id=turma.id)
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.get("/turmas", response_model=list[TurmaSaida])
def minhas_turmas(
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    return (
        db.query(Turma)
        .join(Matricula, Matricula.turma_id == Turma.id)
        .filter(Matricula.aluno_id == aluno.id)
        .all()
    )


def _validar_matricula(db: Session, aluno_id: int, turma_id: int) -> None:
    matricula = (
        db.query(Matricula)
        .filter(Matricula.aluno_id == aluno_id, Matricula.turma_id == turma_id)
        .first()
    )
    if matricula is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não está matriculado nesta turma.",
        )


# ---------- Chat com o tutor ----------

@router.post("/chat", response_model=ChatRespostaSaida)
def conversar_com_tutor(
    dados: ChatPerguntaInput,
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    """
    A restrição de conteúdo (só materiais liberados para a turma) é
    aplicada dentro de rag_service.responder_pergunta_aluno — esta rota
    apenas garante que o aluno pertence à turma antes de prosseguir.
    """
    _validar_matricula(db, aluno.id, dados.turma_id)

    if dados.sessao_id:
        sessao = (
            db.query(SessaoChat)
            .filter(
                SessaoChat.id == dados.sessao_id,
                SessaoChat.aluno_id == aluno.id,
                SessaoChat.turma_id == dados.turma_id,
            )
            .first()
        )
        if sessao is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão de chat não encontrada.")
    else:
        sessao = SessaoChat(aluno_id=aluno.id, turma_id=dados.turma_id)
        db.add(sessao)
        db.flush()

    db.add(Mensagem(sessao_id=sessao.id, remetente=RemetenteMensagem.ALUNO, conteudo=dados.pergunta))

    resposta_texto, material_ids_usados = responder_pergunta_aluno(db, dados.turma_id, dados.pergunta)

    db.add(
        Mensagem(
            sessao_id=sessao.id,
            remetente=RemetenteMensagem.ASSISTENTE,
            conteudo=resposta_texto,
            materiais_utilizados=",".join(str(m) for m in material_ids_usados),
        )
    )
    db.commit()

    return ChatRespostaSaida(
        sessao_id=sessao.id, resposta=resposta_texto, materiais_utilizados=material_ids_usados
    )


@router.get("/chat/sessoes/{sessao_id}", response_model=SessaoChatSaida)
def obter_historico_sessao(
    sessao_id: int,
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    sessao = (
        db.query(SessaoChat)
        .filter(SessaoChat.id == sessao_id, SessaoChat.aluno_id == aluno.id)
        .first()
    )
    if sessao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sessão não encontrada.")
    return sessao


# ---------- Simulados ----------

@router.get("/turmas/{turma_id}/simulados", response_model=list[SimuladoSaida])
def listar_simulados_da_turma(
    turma_id: int,
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    _validar_matricula(db, aluno.id, turma_id)
    return db.query(Simulado).filter(Simulado.turma_id == turma_id).all()


@router.post("/simulados/{simulado_id}/responder", response_model=TentativaSaida)
def responder_simulado(
    simulado_id: int,
    dados: ResponderSimuladoInput,
    aluno: Usuario = Depends(exigir_aluno),
    db: Session = Depends(get_db),
):
    simulado = db.query(Simulado).filter(Simulado.id == simulado_id).first()
    if simulado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Simulado não encontrado.")

    _validar_matricula(db, aluno.id, simulado.turma_id)

    questoes = {q.id: q for q in simulado.questoes}
    if set(dados.respostas.keys()) != set(questoes.keys()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="É necessário responder todas as questões do simulado.",
        )

    acertos = sum(
        1 for qid, resposta in dados.respostas.items() if questoes[qid].resposta_correta == resposta
    )
    nota = round((acertos / len(questoes)) * 10, 2)

    tentativa = TentativaSimulado(
        simulado_id=simulado.id,
        aluno_id=aluno.id,
        respostas=dados.respostas,
        nota=nota,
    )
    db.add(tentativa)
    db.commit()
    db.refresh(tentativa)

    questoes_com_gabarito = [
        QuestaoComGabaritoSaida.model_validate(q, from_attributes=True) for q in simulado.questoes
    ]

    return TentativaSaida(
        id=tentativa.id,
        simulado_id=tentativa.simulado_id,
        nota=tentativa.nota,
        finalizado_em=tentativa.finalizado_em,
        questoes_com_gabarito=questoes_com_gabarito,
    )
