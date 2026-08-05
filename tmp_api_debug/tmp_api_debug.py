import os, sys
os.environ.setdefault('GEMINI_API_KEY', 'test')
sys.path.insert(0, r'C:\VScode\ChronosBot\backend')
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
r = client.post('/auth/registrar', json={'nome':'Teste Prof Debug', 'email':'teste.prof.debug@example.com', 'senha':'Senha123', 'papel':'professor'})
print('registro', r.status_code, r.text)
l = client.post('/auth/login', data={'username':'teste.prof.debug@example.com', 'password':'Senha123'})
print('login', l.status_code, l.text)
token = l.json().get('access_token') if l.status_code == 200 else None
print('token', token)
headers = {'Authorization': f'Bearer {token}', 'Origin':'http://localhost:5173'} if token else {'Origin':'http://localhost:5173'}
m = client.get('/professor/materiais', headers=headers)
print('materiais', m.status_code, m.text)
print('headers', dict(m.headers))
