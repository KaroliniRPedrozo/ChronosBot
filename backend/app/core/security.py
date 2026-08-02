"""
Funções de autenticação e segurança.

Princípio arquitetural: a identidade do usuário SEMPRE vem do JWT decodificado
no backend, nunca de campos enviados no corpo da requisição. Isso impede que um
usuário mal-intencionado se passe por outro simplesmente alterando o payload.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
import hmac
import secrets
from passlib.context import CryptContext

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.usuario import Usuario, PapelUsuario

HASH_NAME = "sha256"
ITERATIONS = 150000
SALT_BYTES = 16

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------- Senhas ----------

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt", "argon2"], deprecated="auto")


def hash_senha(senha_plana: str) -> str:
    salt = secrets.token_hex(SALT_BYTES)
    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_NAME,
        senha_plana.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS,
    )
    hash_hex = hash_bytes.hex()
    return f"pbkdf2_sha256${ITERATIONS}${salt}${hash_hex}"


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica senha suportando o formato interno `pbkdf2_sha256$it$salt$hash`.

    Se o hash não corresponder ao formato interno, faz um fallback para
    `passlib` para suportar hashes legados (bcrypt/argon2/etc.).
    """
    # Try native pbkdf2 format first
    try:
        if senha_hash.startswith("pbkdf2_sha256$"):
            scheme, iterations, salt, expected = senha_hash.split("$")
            if scheme != "pbkdf2_sha256":
                return False
            derived = hashlib.pbkdf2_hmac(
                HASH_NAME,
                senha_plana.encode("utf-8"),
                salt.encode("utf-8"),
                int(iterations),
            ).hex()
            return hmac.compare_digest(derived, expected)
    except Exception:
        # Fall through to passlib fallback
        pass

    # Fallback: try passlib context to verify common legacy hashes
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except Exception:
        return False


# ---------- JWT ----------

def criar_access_token(dados: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um JWT contendo, no mínimo: sub (id do usuário), papel, e exp.
    """
    to_encode = dados.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decodificar_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


# ---------- Dependencies de identidade (usadas nas rotas) ----------

def get_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """
    Extrai o usuário autenticado a partir do token JWT.
    Esta é A fonte única de identidade em toda a aplicação — nenhuma rota
    deve aceitar um `usuario_id` vindo do corpo da requisição.
    """
    payload = decodificar_token(token)
    usuario_id = int(payload["sub"])

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
        )
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada.",
        )
    return usuario


def exigir_professor(usuario: Usuario = Depends(get_usuario_atual)) -> Usuario:
    if usuario.papel != PapelUsuario.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a professores.",
        )
    return usuario


def exigir_aluno(usuario: Usuario = Depends(get_usuario_atual)) -> Usuario:
    if usuario.papel != PapelUsuario.ALUNO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a alunos.",
        )
    return usuario
