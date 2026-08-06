import os
from pathlib import Path
from sqlalchemy import create_engine, text

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
print('DB URL:', url)
if not url:
    raise SystemExit('DATABASE_URL not found in backend/.env')

engine = create_engine(url)
with engine.connect() as conn:
    print('USERS:')
    rows = conn.execute(
        text(
            "select id, nome, email, papel from usuarios where email in ('profana@escola.local','profcarlos@escola.local','alice@escola.local','bruno@escola.local','camila@escola.local')"
        )
    ).fetchall()
    for row in rows:
        print(row)

    print('TURMAS:')
    rows = conn.execute(
        text(
            "select id, nome, disciplina, codigo_convite, professor_id from turmas where codigo_convite in ('6A-HIST','7B-GEO','8C-HIST')"
        )
    ).fetchall()
    for row in rows:
        print(row)
