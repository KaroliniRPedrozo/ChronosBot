from pydantic import BaseModel, EmailStr, ConfigDict, Field
from backend.app.models.usuario import PapelUsuario


class UsuarioCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    email: EmailStr
    senha: str = Field(min_length=8, description="Mínimo de 8 caracteres.")
    papel: PapelUsuario


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    # aceita e-mails de teste (ex.: alice@escola.local)
    email: str
    papel: PapelUsuario
    ativo: bool


class TokenSaida(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioSaida
