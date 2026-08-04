"""Seed de dados de teste para o ChronosBot.

Cria:
- 1 professor com 2 ou mais turmas
- 1 professor com 1 turma
- 3 alunos divididos entre as turmas

Execute a partir da pasta backend:
    ..\venv\Scripts\python.exe seed_test_data.py
"""

import sys
from pathlib import Path

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.database import SessionLocal, engine, Base
from backend.app.core.security import hash_senha
from backend.app.models.usuario import Usuario, PapelUsuario
from backend.app.models.turma import Turma, Disciplina, Matricula


def _constraint_exists(conn, table_name: str, constraint_name: str) -> bool:
    result = conn.execute(
        text(
            "SELECT 1 FROM information_schema.table_constraints "
            "WHERE table_name = :table_name AND constraint_name = :constraint_name"
        ),
        {"table_name": table_name, "constraint_name": constraint_name},
    )
    return result.first() is not None


def _column_exists(conn, table_name: str, column_name: str) -> bool:
    result = conn.execute(
        text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = :table_name AND column_name = :column_name"
        ),
        {"table_name": table_name, "column_name": column_name},
    )
    return result.first() is not None


def reparar_esquema_antigo():
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS papel VARCHAR(50)"))
        conn.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS ativo BOOLEAN DEFAULT TRUE"))
        conn.execute(text("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()"))
        conn.execute(text("UPDATE usuarios SET papel = role WHERE papel IS NULL AND role IS NOT NULL"))
        conn.execute(text("UPDATE usuarios SET papel = 'aluno' WHERE papel IS NULL"))
        conn.execute(text("ALTER TABLE usuarios ALTER COLUMN papel SET NOT NULL"))
        conn.execute(text("ALTER TABLE usuarios ALTER COLUMN ativo SET NOT NULL"))

        conn.execute(text("ALTER TABLE turmas ADD COLUMN IF NOT EXISTS disciplina VARCHAR(50)"))
        conn.execute(text("ALTER TABLE turmas ADD COLUMN IF NOT EXISTS codigo_convite VARCHAR(50)"))
        conn.execute(text("ALTER TABLE turmas ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()"))
        conn.execute(text("UPDATE turmas SET disciplina = 'Historia' WHERE disciplina IS NULL"))
        conn.execute(text("UPDATE turmas SET codigo_convite = 'TURMA-' || id WHERE codigo_convite IS NULL"))
        conn.execute(text("ALTER TABLE turmas ALTER COLUMN disciplina SET NOT NULL"))
        conn.execute(text("ALTER TABLE turmas ALTER COLUMN codigo_convite SET NOT NULL"))
        if not _constraint_exists(conn, "turmas", "uq_turmas_codigo_convite"):
            conn.execute(text("ALTER TABLE turmas ADD CONSTRAINT uq_turmas_codigo_convite UNIQUE (codigo_convite)"))

        conn.execute(text("ALTER TABLE materiais ADD COLUMN IF NOT EXISTS disciplina VARCHAR(50)"))
        conn.execute(text("ALTER TABLE materiais ADD COLUMN IF NOT EXISTS professor_id INTEGER"))
        conn.execute(text("ALTER TABLE materiais ADD COLUMN IF NOT EXISTS status_processamento VARCHAR(50) DEFAULT 'pendente'"))
        conn.execute(text("ALTER TABLE materiais ADD COLUMN IF NOT EXISTS mensagem_erro TEXT"))

        if _column_exists(conn, "materiais", "turma_id"):
            conn.execute(text(
                "UPDATE materiais SET disciplina = turmas.disciplina, professor_id = turmas.professor_id "
                "FROM turmas WHERE materiais.turma_id = turmas.id AND materiais.disciplina IS NULL"
            ))

        conn.execute(text("UPDATE materiais SET disciplina = 'Historia' WHERE disciplina IS NULL"))

        if _column_exists(conn, "materiais", "processado"):
            conn.execute(text(
                "UPDATE materiais SET status_processamento = CASE WHEN processado IS TRUE THEN 'concluido' ELSE 'pendente' END "
                "WHERE status_processamento IS NULL"
            ))

        conn.execute(text(
            "UPDATE materiais SET professor_id = (SELECT id FROM usuarios WHERE papel = 'professor' LIMIT 1) "
            "WHERE professor_id IS NULL"
        ))

        conn.execute(text("ALTER TABLE materiais ADD COLUMN IF NOT EXISTS criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()"))
        conn.execute(text("UPDATE materiais SET criado_em = now() WHERE criado_em IS NULL"))
        conn.execute(text("ALTER TABLE materiais ALTER COLUMN criado_em SET DEFAULT now()"))
        conn.execute(text("ALTER TABLE materiais ALTER COLUMN criado_em SET NOT NULL"))

        if _column_exists(conn, "materiais", "data_liberacao"):
            conn.execute(text("ALTER TABLE materiais DROP COLUMN IF EXISTS data_liberacao"))
        conn.execute(text("ALTER TABLE materiais ALTER COLUMN disciplina SET NOT NULL"))
        conn.execute(text("ALTER TABLE materiais ALTER COLUMN professor_id SET NOT NULL"))
        conn.execute(text("ALTER TABLE materiais ALTER COLUMN status_processamento SET NOT NULL"))
        conn.execute(text("ALTER TABLE materiais DROP COLUMN IF EXISTS turma_id"))
        conn.execute(text("ALTER TABLE materiais DROP COLUMN IF EXISTS processado"))


def criar_usuario(db, nome, email, senha, papel):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return usuario
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha),
        papel=papel,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def criar_turma(db, nome, disciplina, professor, codigo_convite):
    turma = db.query(Turma).filter(Turma.codigo_convite == codigo_convite).first()
    if turma:
        return turma
    turma = Turma(
        nome=nome,
        disciplina=disciplina,
        professor_id=professor.id,
        codigo_convite=codigo_convite,
    )
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma


def matricular_aluno(db, aluno, turma):
    existe = (
        db.query(Matricula)
        .filter(Matricula.aluno_id == aluno.id, Matricula.turma_id == turma.id)
        .first()
    )
    if existe:
        return existe
    matricula = Matricula(aluno_id=aluno.id, turma_id=turma.id)
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


def main():
    print("Reparando esquema legado e criando tabelas ausentes...")
    reparar_esquema_antigo()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Criando professores de teste...")
        prof_multiturma = criar_usuario(
            db,
            nome="Prof. Ana Silva",
            email="profana@escola.local",
            senha="Prof123456!",
            papel=PapelUsuario.PROFESSOR,
        )
        prof_uma_turma = criar_usuario(
            db,
            nome="Prof. Carlos Lima",
            email="profcarlos@escola.local",
            senha="Prof123456!",
            papel=PapelUsuario.PROFESSOR,
        )

        print("Criando turmas de teste...")
        turma_6a = criar_turma(
            db,
            nome="6º Ano A - História",
            disciplina=Disciplina.HISTORIA,
            professor=prof_multiturma,
            codigo_convite="6A-HIST",
        )
        turma_7b = criar_turma(
            db,
            nome="7º Ano B - Geografia",
            disciplina=Disciplina.GEOGRAFIA,
            professor=prof_multiturma,
            codigo_convite="7B-GEO",
        )
        turma_8c = criar_turma(
            db,
            nome="8º Ano C - História",
            disciplina=Disciplina.HISTORIA,
            professor=prof_uma_turma,
            codigo_convite="8C-HIST",
        )

        print("Criando alunos de teste...")
        aluno1 = criar_usuario(
            db,
            nome="Alice Souza",
            email="alice@escola.local",
            senha="Aluno1234!",
            papel=PapelUsuario.ALUNO,
        )
        aluno2 = criar_usuario(
            db,
            nome="Bruno Ferreira",
            email="bruno@escola.local",
            senha="Aluno1234!",
            papel=PapelUsuario.ALUNO,
        )
        aluno3 = criar_usuario(
            db,
            nome="Camila Pinto",
            email="camila@escola.local",
            senha="Aluno1234!",
            papel=PapelUsuario.ALUNO,
        )

        print("Matriculando alunos nas turmas...")
        matricular_aluno(db, aluno1, turma_6a)
        matricular_aluno(db, aluno2, turma_7b)
        matricular_aluno(db, aluno3, turma_8c)

        print("Seed concluída com sucesso!")
        print("Acessos de teste:")
        print("  Professor multiturma: profana@escola.local / Prof123456!")
        print("  Professor 1 turma: profcarlos@escola.local / Prof123456!")
        print("  Aluno 1 (6º Ano A): alice@escola.local / Aluno1234!")
        print("  Aluno 2 (7º Ano B): bruno@escola.local / Aluno1234!")
        print("  Aluno 3 (8º Ano C): camila@escola.local / Aluno1234!")
        print("")
        print("Códigos de convite de turma:")
        print("  6º Ano A - História: 6A-HIST")
        print("  7º Ano B - Geografia: 7B-GEO")
        print("  8º Ano C - História: 8C-HIST")
    finally:
        db.close()


if __name__ == "__main__":
    main()
