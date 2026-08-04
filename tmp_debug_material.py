import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'backend'))
from backend.seed_test_data import main as seed_main
from backend.app.main import app
from fastapi.testclient import TestClient

seed_main()
client = TestClient(app)
r = client.post('/auth/login', data={'username': 'profana@escola.local', 'password': 'Prof123456!'})
print('login status', r.status_code, r.text)
if r.status_code != 200:
    raise SystemExit('login failed')
access_token = r.json()['access_token']
headers = {'Authorization': f'Bearer {access_token}'}
files = {'arquivo': ('teste.txt', b'Hello world', 'text/plain')}
data = {'titulo': 'Teste Material', 'disciplina': 'Historia'}
r = client.post('/professor/materiais', headers=headers, data=data, files=files)
print('upload status', r.status_code, r.text)
