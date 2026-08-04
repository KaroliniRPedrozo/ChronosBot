import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from backend.app.core.config import settings
from sqlalchemy import create_engine, text

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    print('DATABASE_URL=', settings.DATABASE_URL)
    print('MATERIAIS COLUMNS:')
    for row in conn.execute(text("select column_name, is_nullable, data_type from information_schema.columns where table_name='materiais' order by ordinal_position")):
        print(row)
    print('CONSTRAINTS:')
    for row in conn.execute(text("select constraint_name, constraint_type from information_schema.table_constraints where table_name='materiais'")):
        print(row)
    for col in ['turma_id', 'processado', 'data_liberacao', 'professor_id', 'status_processamento']:
        print('EXISTS', col, list(conn.execute(text("select column_name, is_nullable from information_schema.columns where table_name='materiais' and column_name=:col"), {'col': col})))
