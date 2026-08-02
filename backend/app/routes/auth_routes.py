from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import hash_senha, verificar_senha, criar_access_token
from backend.app.models.usuario import Usuario
from backend.app.schemas.usuario import UsuarioCriar, UsuarioSaida, TokenSaida

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar", response_model=UsuarioSaida, status_code=status.HTTP_201_CREATED)
def registrar(dados: UsuarioCriar, db: Session = Depends(get_db)):
    ja_existe = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if ja_existe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        papel=dados.papel,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=TokenSaida)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Usa OAuth2PasswordRequestForm (campos `username`/`password`) para
    compatibilidade com o esquema padrão do FastAPI/Swagger.
    `username` aqui é o e-mail do usuário.
    """
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="E-mail ou senha incorretos.",
    )

    if usuario is None or not verificar_senha(form_data.password, usuario.senha_hash):
        raise credenciais_invalidas

    if not usuario.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta desativada.")

    token = criar_access_token({"sub": str(usuario.id), "papel": usuario.papel.value})
    return TokenSaida(access_token=token, usuario=usuario)
