# ChronosBot — Backend

API do ChronosBot: plataforma de tutoria educacional com IA, restrita às
disciplinas de História e Geografia.

## Setup local (Codespaces ou máquina local)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edite .env com sua DATABASE_URL, JWT_SECRET_KEY e GEMINI_API_KEY

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docs interativas: `http://localhost:8000/docs`

## Estrutura

```
app/
  core/       -> config, conexão com banco, segurança (JWT/bcrypt)
  models/     -> tabelas SQLAlchemy (usuario, turma, material, chat, simulado)
  schemas/    -> validação Pydantic de entrada/saída das rotas
  services/   -> regras de negócio (RAG, Gemini, processamento de material, simulados)
  routes/     -> endpoints da API (auth, professor, aluno)
  main.py     -> ponto de entrada, monta o FastAPI e inclui as rotas
```

## Arquitetura de controle de acesso (importante para a monografia)

O controle de acesso a materiais é resolvido **na camada de dados**, nunca
por instrução de prompt ao LLM:

1. `MaterialTurmaPermissao` decide, por turma, quais `material_id` estão
   liberados e a partir de quando (`data_liberacao`).
2. `rag_service.obter_materiais_permitidos()` faz a consulta relacional
   **primeiro**.
3. Só então `rag_service.buscar_trechos_relevantes()` consulta o ChromaDB,
   restringindo a busca vetorial (`where={"material_id": {"$in": [...]}}`)
   aos IDs já aprovados.

Isso garante que o modelo Gemini nunca recebe, no contexto, conteúdo que o
aluno não deveria ver — mesmo que o prompt do sistema falhe ou seja
manipulado, o vazamento é estruturalmente impossível.

## Identidade sempre via JWT

Nenhuma rota aceita `usuario_id`/`professor_id`/`aluno_id` vindo do corpo
da requisição. A identidade é sempre extraída do token JWT decodificado em
`core/security.py` (`get_usuario_atual`, `exigir_professor`, `exigir_aluno`).

## Rotas principais

- `POST /auth/registrar`, `POST /auth/login`
- `POST /professor/turmas`, `GET /professor/turmas`
- `POST /professor/materiais` (upload), `POST /professor/materiais/{id}/liberar`
- `POST /professor/simulados` (geração via Gemini)
- `POST /aluno/turmas/entrar`, `GET /aluno/turmas`
- `POST /aluno/chat` (tutor IA), `GET /aluno/chat/sessoes/{id}`
- `GET /aluno/turmas/{id}/simulados`, `POST /aluno/simulados/{id}/responder`

## Decisão em aberto: processamento síncrono vs. background

Implementado com `BackgroundTasks` do FastAPI (ver nota completa em
`services/material_service.py`). Suficiente para o escopo do TCC; migração
para Celery/RQ fica documentada como trabalho futuro.

## Testes rápidos (smoke tests)

Para facilitar a verificação local e resolver os avisos do Pylance sobre
imports, siga estas etapas:

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

O repositório inclui um teste de smoke em `app/tests/test_smoke.py` que
verifica as rotas `/` e `/health`. Se o VS Code ainda mostrar erros do
Pylance para imports como `backend.app`, reinicie o servidor de linguagem
ou selecione o interpretador Python do venv (a configuração sugerida está
em `.vscode/settings.json`).
