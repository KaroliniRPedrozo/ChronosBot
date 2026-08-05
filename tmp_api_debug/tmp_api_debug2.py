import os, sys
sys.path.insert(0, r'C:\VScode\ChronosBot\backend')
os.environ.setdefault('GEMINI_API_KEY', 'test')
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
r = client.post('/auth/login', data={'username':'teste.prof@example.com','password':'Senha123'})
print('login', r.status_code, r.text)
token = r.json().get('access_token') if r.status_code == 200 else None
headers = {'Authorization': f'Bearer {token}', 'Origin': 'http://localhost:5173'} if token else {'Origin': 'http://localhost:5173'}
m = client.get('/professor/materiais', headers=headers)
print('materiais', m.status_code, m.text)
print('headers', dict(m.headers))
