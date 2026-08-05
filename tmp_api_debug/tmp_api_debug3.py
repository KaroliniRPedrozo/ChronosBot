import os, sys
sys.path.insert(0, r'C:\VScode\ChronosBot\backend')
os.environ.setdefault('GEMINI_API_KEY', 'test')
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
# Ensure professor exists and can login
email = 'teste.prof@example.com'
password = 'Senha123'
resp = client.post('/auth/login', data={'username': email, 'password': password})
if resp.status_code != 200:
    client.post('/auth/registrar', json={'nome':'Teste Prof', 'email': email, 'senha': password, 'papel': 'professor'})
    resp = client.post('/auth/login', data={'username': email, 'password': password})
print('login', resp.status_code, resp.text)
token = resp.json().get('access_token')
headers = {'Authorization': f'Bearer {token}', 'Origin': 'http://localhost:5173'}
files = {'arquivo': ('teste.txt', b'Teste de upload', 'text/plain')}
data = {'titulo': 'Teste Material', 'disciplina': 'Historia'}
res = client.post('/professor/materiais', headers=headers, data=data, files=files)
print('status', res.status_code)
print('headers', dict(res.headers))
print('body', res.text)
