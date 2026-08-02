from backend.app.models.usuario import Usuario, PapelUsuario
from backend.app.models.turma import Turma, Matricula, Disciplina
from backend.app.models.material import Material, MaterialTurmaPermissao, StatusProcessamento
from backend.app.models.chat import SessaoChat, Mensagem, RemetenteMensagem
from backend.app.models.simulado import Simulado, Questao, TentativaSimulado

__all__ = [
    "Usuario", "PapelUsuario",
    "Turma", "Matricula", "Disciplina",
    "Material", "MaterialTurmaPermissao", "StatusProcessamento",
    "SessaoChat", "Mensagem", "RemetenteMensagem",
    "Simulado", "Questao", "TentativaSimulado",
]
