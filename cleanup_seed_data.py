import os
from pathlib import Path
from sqlalchemy import create_engine, text

# Load DB URL from backend/.env
path = Path('backend') / '.env'
config = {}
if path.exists():
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        config[key.strip()] = value.strip()

url = config.get('DATABASE_URL')
if not url:
    raise SystemExit('DATABASE_URL not found in backend/.env')

engine = create_engine(url)
with engine.begin() as conn:
    seed_emails = [
        'profana@escola.local',
        'profcarlos@escola.local',
        'alice@escola.local',
        'bruno@escola.local',
        'camila@escola.local',
    ]
    seed_codes = ['6A-HIST', '7B-GEO', '8C-HIST']

    print('Inspecting seed data...')
    user_ids = [row[0] for row in conn.execute(text(
        "select id from usuarios where email in :emails"
    ), {'emails': tuple(seed_emails)}).fetchall()]
    turma_ids = [row[0] for row in conn.execute(text(
        "select id from turmas where codigo_convite in :codes"
    ), {'codes': tuple(seed_codes)}).fetchall()]

    print('Seed user IDs:', user_ids)
    print('Seed class IDs:', turma_ids)

    if not user_ids and not turma_ids:
        print('No seed users or classes found. Nothing to delete.')
    else:
        # Find materials by seed professors
        material_ids = [row[0] for row in conn.execute(text(
            "select id from materiais where professor_id in :user_ids"
        ), {'user_ids': tuple(user_ids)}).fetchall()]
        print('Seed material IDs:', material_ids)

        # Find simulados by seed classes or professors
        simulado_ids = [row[0] for row in conn.execute(text(
            "select id from simulados where turma_id in :turma_ids or criado_por_id in :user_ids"
        ), {'turma_ids': tuple(turma_ids), 'user_ids': tuple(user_ids)}).fetchall()]
        print('Seed simulado IDs:', simulado_ids)

        # Delete related records in proper order
        if simulado_ids:
            conn.execute(text("delete from questoes where simulado_id in :simulado_ids"), {'simulado_ids': tuple(simulado_ids)})
            conn.execute(text("delete from tentativas_simulado where simulado_id in :simulado_ids"), {'simulado_ids': tuple(simulado_ids)})
            conn.execute(text("delete from simulados where id in :simulado_ids"), {'simulado_ids': tuple(simulado_ids)})

        if user_ids:
            conn.execute(text("delete from mensagens where sessao_id in (select id from sessoes_chat where aluno_id in :user_ids)"), {'user_ids': tuple(user_ids)})
            conn.execute(text("delete from sessoes_chat where aluno_id in :user_ids"), {'user_ids': tuple(user_ids)})
            conn.execute(text("delete from tentativas_simulado where aluno_id in :user_ids"), {'user_ids': tuple(user_ids)})

        if material_ids:
            conn.execute(text("delete from material_turma_permissao where material_id in :material_ids"), {'material_ids': tuple(material_ids)})
            conn.execute(text("delete from materiais where id in :material_ids"), {'material_ids': tuple(material_ids)})

        if turma_ids:
            conn.execute(text("delete from material_turma_permissao where turma_id in :turma_ids"), {'turma_ids': tuple(turma_ids)})
            conn.execute(text("delete from matriculas where turma_id in :turma_ids"), {'turma_ids': tuple(turma_ids)})
            conn.execute(text("delete from turmas where id in :turma_ids"), {'turma_ids': tuple(turma_ids)})

        if user_ids:
            conn.execute(text("delete from matriculas where aluno_id in :user_ids"), {'user_ids': tuple(user_ids)})
            conn.execute(text("delete from usuarios where id in :user_ids"), {'user_ids': tuple(user_ids)})

        print('Seed users and classes deleted successfully.')
