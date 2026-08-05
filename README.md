<a name="topo"></a>
<h1 align="center">
  <img src="https://github.com/KaroliniRPedrozo/ChronosBot/blob/main/frontend/src/assets/logo.png" width="100" alt="ChronosBot Logo"><br>
  ChronosBot
</h1>

**Plataforma de tutoria inteligente com RAG — onde professores ensinam a IA e a IA ensina os alunos.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=white)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![pgvector](https://img.shields.io/badge/pgvector-VectorDB-4169E1?style=flat-square)](https://github.com/pgvector/pgvector)
[![Gemini](https://img.shields.io/badge/Gemini-API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)

---

## 📑 Sumário

- [📊 Status de Desenvolvimento](#-status-de-desenvolvimento)
- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🏗️ Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [🗄️ Esquema do Banco de Dados](#️-esquema-do-banco-de-dados-postgresql--pgvector)
- [🧠 Lógica RAG com Filtro Temporal](#-lógica-rag-com-filtro-temporal-python)
- [🔑 Rotação de Chaves Gemini](#-rotação-de-chaves-gemini-free-tier)
- [📝 Modo Simulado](#-modo-simulado-geração-de-quiz-com-gemini)
- [🛣️ Rotas da API](#️-rotas-da-api-fastapi)
- [🚀 Guia Completo de Instalação](#-guia-completo-de-instalação-passo-a-passo)
  - [1. Pré-requisitos (o que baixar)](#1-pré-requisitos-o-que-baixar)
  - [2. Clonar o repositório](#2-clonar-o-repositório)
  - [3. Configurar o PostgreSQL + pgvector](#3-configurar-o-postgresql--pgvector)
  - [4. Configurar o Backend](#4-configurar-o-backend)
  - [5. Configurar o Frontend](#5-configurar-o-frontend)
  - [6. Rodar o projeto](#6-rodar-o-projeto)
  - [7. Verificação final](#7-verificação-final)
  - [Problemas comuns](#️-problemas-comuns)
- [🗂️ Estrutura do Projeto](#️-estrutura-do-projeto)
- [🔒 Segurança e Conformidade](#-segurança-e-conformidade)
- [📊 Métricas de Qualidade](#-métricas-de-qualidade-isoiec-25010)
- [🤝 Contribuindo](#-contribuindo)

---

## 📊 Status de Desenvolvimento

| Módulo | Status | Progresso |
| ------ | ------ | --------- |
| 🗄️ Banco de Dados (Modelos & Esquema) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🔐 Autenticação (JWT / RBAC) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🧠 Motor RAG (pgvector — Indexação & Retrieval) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🔑 Rotação de Chaves Gemini (free tier) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 📝 Modo Simulado (Quiz) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🛣️ Rotas do Professor | 🔄 Em andamento | ![80%](https://img.shields.io/badge/80%25-yellow?style=flat-square) |
| 🛣️ Rotas do Aluno | 🔄 Em andamento | ![80%](https://img.shields.io/badge/80%25-yellow?style=flat-square) |
| ⚙️ Backend (Integração Geral) | 🔄 Em andamento | ![85%](https://img.shields.io/badge/85%25-yellow?style=flat-square) |
| 🌐 Frontend (React + páginas legadas HTML) | 🔄 Em andamento | ![70%](https://img.shields.io/badge/70%25-orange?style=flat-square) |
| 🧪 Testes & Validação | ⏳ Pendente | ![0%](https://img.shields.io/badge/0%25-lightgrey?style=flat-square) |

> **Versão atual:** `0.7-beta` · **Última atualização:** Agosto/2026


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 📖 Sobre o Projeto

O **ChronosBot** é uma plataforma educacional full-stack desenvolvida como Trabalho de Conclusão de Curso (TCC), que une **Geração Aumentada por Recuperação (RAG)** com controle pedagógico real. O sistema atua especificamente nas disciplinas de **História e Geografia**, permitindo que professores façam upload de seus materiais, definam datas de liberação por turma e a IA responda — **somente** com o que já foi ensinado até aquele momento.

> *"Um agente conversacional não é apenas o que responde, mas também o que escolhe não responder ainda."*

### 🎯 Escopo Curricular

O tutor inteligente é especializado nas seguintes disciplinas da Educação Básica:

| Disciplina | Conteúdos Suportados |
| ---------- | -------------------- |
| 📜 **História** | História do Brasil, História Geral, Linha do Tempo, Fontes Históricas |
| 🌍 **Geografia** | Geografia Física, Geopolítica, Cartografia, Meio Ambiente e Sustentabilidade |

> Perguntas fora dessas disciplinas são educadamente recusadas pelo tutor, mantendo o foco pedagógico.


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## ✨ Funcionalidades

### 👩‍🏫 Perfil Professor

- Criação e gestão de turmas (ex: `6º Ano A`, `Turma de História`)
- Upload de materiais em PDF/TXT que alimentam a base RAG
- **Controle de liberação por data** — o aluno só acessa o conteúdo na data definida pelo professor
- Dashboard com métricas de uso por turma

### 🎓 Perfil Aluno

- Cadastro com vínculo automático à turma
- **Chat Tutor** — a IA responde apenas com base nos materiais de História e Geografia já liberados
- **Modo Simulado** — geração de quiz de múltipla escolha com base no conteúdo estudado
- Histórico de sessões e desempenho nos simulados


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🏗️ Arquitetura do Sistema

```text
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│      React (SPA) + páginas HTML legadas em migração         │
└─────────────────┬────────────────────┬──────────────────────┘
                  │ REST / WebSocket   │ SSE (streaming)
┌─────────────────▼────────────────────▼──────────────────────┐
│                    BACKEND (FastAPI / Python)               │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Auth & RBAC  │  │  RAG Engine  │  │  Simulado Engine  │  │
│  └──────────────┘  └──────┬───────┘  └─────────┬─────────┘  │
└──────────────────────────────────────────────────────────────┘
                             │                     │
          ┌──────────────────┘                     │
          ▼                                        ▼
┌──────────────────────────┐          ┌──────────────────────────┐
│  PostgreSQL + pgvector   │          │  Google Gemini API       │
│  dados relacionais +     │          │  (LLM + Embeddings)      │
│  embeddings na mesma base│          │  com rotação de chaves   │
└──────────────────────────┘          └──────────────────────────┘
```

> **Por que pgvector em vez de um banco vetorial separado?** Mantém dados relacionais (turmas, permissões, datas de liberação) e embeddings na mesma transação/banco, simplificando deploy e garantindo consistência entre metadado e vetor.


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🗄️ Esquema do Banco de Dados (PostgreSQL + pgvector)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Professores e Alunos
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome        VARCHAR(255) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    senha_hash  TEXT NOT NULL,
    role        VARCHAR(20) CHECK (role IN ('professor', 'aluno')),
    criado_em   TIMESTAMPTZ DEFAULT NOW()
);

-- Turmas criadas pelos professores
CREATE TABLE turmas (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome           VARCHAR(255) NOT NULL,
    professor_id   UUID REFERENCES users(id) ON DELETE CASCADE,
    criado_em      TIMESTAMPTZ DEFAULT NOW()
);

-- Vínculo aluno ↔ turma
CREATE TABLE alunos_turmas (
    aluno_id   UUID REFERENCES users(id) ON DELETE CASCADE,
    turma_id   UUID REFERENCES turmas(id) ON DELETE CASCADE,
    PRIMARY KEY (aluno_id, turma_id)
);

-- Materiais enviados pelos professores
CREATE TABLE arquivos (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    turma_id         UUID REFERENCES turmas(id) ON DELETE CASCADE,
    nome_arquivo     VARCHAR(255) NOT NULL,
    caminho_storage  TEXT NOT NULL,
    disciplina       VARCHAR(50) CHECK (disciplina IN ('historia', 'geografia')),
    data_liberacao   DATE NOT NULL,
    indexado         BOOLEAN DEFAULT FALSE,
    criado_em        TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks indexados com embeddings (pgvector)
CREATE TABLE chunks_rag (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    arquivo_id    UUID REFERENCES arquivos(id) ON DELETE CASCADE,
    turma_id      UUID REFERENCES turmas(id) ON DELETE CASCADE,
    disciplina    VARCHAR(50) CHECK (disciplina IN ('historia', 'geografia')),
    data_liberacao DATE NOT NULL,
    conteudo      TEXT NOT NULL,
    embedding     VECTOR(768),   -- dimensão do modelo de embeddings do Gemini
    criado_em     TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_chunks_embedding ON chunks_rag USING ivfflat (embedding vector_cosine_ops);

-- Sessões de chat dos alunos
CREATE TABLE sessoes_chat (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id      UUID REFERENCES users(id),
    turma_id      UUID REFERENCES turmas(id),
    iniciado_em   TIMESTAMPTZ DEFAULT NOW(),
    encerrado_em  TIMESTAMPTZ
);

-- Resultados dos simulados
CREATE TABLE simulados (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aluno_id        UUID REFERENCES users(id),
    turma_id        UUID REFERENCES turmas(id),
    disciplina      VARCHAR(50) CHECK (disciplina IN ('historia', 'geografia')),
    questoes_json   JSONB NOT NULL,
    respostas_json  JSONB,
    pontuacao       NUMERIC(5,2),
    criado_em       TIMESTAMPTZ DEFAULT NOW()
);
```


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🧠 Lógica RAG com Filtro Temporal (Python)

A recuperação de documentos aplica **dois filtros obrigatórios** antes de qualquer consulta ao LLM: o vínculo da turma e a data de liberação. Isso garante que a IA nunca acesse conteúdo de outra turma ou de datas futuras.

```python
# rag/retriever.py
from datetime import date
from pydantic import BaseModel
from google import genai
from sqlalchemy import select, and_
from ..database import get_session
from ..models import ChunkRAG
from .key_rotation import get_active_gemini_client  # rotação de chaves p/ free tier

DISCIPLINAS_PERMITIDAS = {"historia", "geografia"}


class ContextoRecuperado(BaseModel):
    """Resultado tipado da busca vetorial (Pydantic v2)."""
    trechos: list[str]
    turma_id: str
    disciplina: str


def gerar_embedding(texto: str) -> list[float]:
    client = get_active_gemini_client()
    resultado = client.models.embed_content(
        model="text-embedding-004",
        contents=texto,
    )
    return resultado.embeddings[0].values


def recuperar_contexto(
    pergunta: str,
    turma_id: str,
    disciplina: str,
    n_resultados: int = 5,
) -> ContextoRecuperado:
    """
    Recupera chunks relevantes APENAS dos materiais de História ou Geografia
    vinculados à turma do aluno e já liberados até a data atual.

    Args:
        pergunta:     Texto da dúvida do aluno.
        turma_id:     UUID da turma à qual o aluno pertence.
        disciplina:   "historia" ou "geografia".
        n_resultados: Número de chunks a recuperar.

    Returns:
        ContextoRecuperado com os trechos relevantes encontrados.

    Raises:
        ValueError: Se a disciplina solicitada não for suportada.
    """
    if disciplina not in DISCIPLINAS_PERMITIDAS:
        raise ValueError(
            f"Disciplina '{disciplina}' não suportada. "
            f"Opções válidas: {DISCIPLINAS_PERMITIDAS}"
        )

    hoje = date.today()
    vetor_pergunta = gerar_embedding(pergunta)

    with get_session() as session:
        stmt = (
            select(ChunkRAG)
            .where(
                and_(
                    ChunkRAG.turma_id == turma_id,
                    ChunkRAG.disciplina == disciplina,
                    ChunkRAG.data_liberacao <= hoje,
                )
            )
            .order_by(ChunkRAG.embedding.cosine_distance(vetor_pergunta))
            .limit(n_resultados)
        )
        chunks = session.execute(stmt).scalars().all()

    return ContextoRecuperado(
        trechos=[c.conteudo for c in chunks],
        turma_id=turma_id,
        disciplina=disciplina,
    )
```


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🔑 Rotação de Chaves Gemini (Free Tier)

Como o projeto roda no tier gratuito da API Gemini, um pool de chaves é rotacionado automaticamente ao atingir limites de quota, evitando interrupção do serviço em picos de uso (ex: véspera de simulado).

```python
# rag/key_rotation.py
import itertools
from google import genai
from ..config import settings

_pool_chaves = itertools.cycle(settings.GEMINI_API_KEYS)  # lista de chaves no .env


def get_active_gemini_client() -> genai.Client:
    """Retorna um client Gemini usando a próxima chave disponível do pool."""
    chave_atual = next(_pool_chaves)
    return genai.Client(api_key=chave_atual)
```

> ⚠️ **Nota de segurança:** as chaves de API nunca devem ser commitadas no repositório. Use `.env` (ignorado via `.gitignore`) e, se alguma chave já foi exposta em um commit anterior, revogue-a no Google AI Studio e reescreva o histórico do Git (`git filter-repo` ou BFG Repo-Cleaner) antes de tornar o repositório público.


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 📝 Modo Simulado (Geração de Quiz com Gemini)

```python
# rag/simulado.py
import json
from .retriever import recuperar_contexto
from .key_rotation import get_active_gemini_client

PROMPT_SIMULADO = """Você é um examinador rigoroso e imparcial de {disciplina}.
Com base EXCLUSIVAMENTE no contexto abaixo, crie {n_questoes} questões
de múltipla escolha para avaliar o aluno.

Regras obrigatórias:
- Cada questão deve ter 4 alternativas (A, B, C, D)
- Apenas uma alternativa está correta
- NÃO invente informações fora do contexto fornecido
- Varie os níveis cognitivos: compreensão, aplicação e análise
- Responda SOMENTE em JSON válido, sem texto extra ou markdown

Formato de saída:
{{
  "disciplina": "{disciplina}",
  "questoes": [
    {{
      "enunciado": "...",
      "alternativas": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "gabarito": "A",
      "justificativa": "..."
    }}
  ]
}}

--- CONTEXTO ---
{contexto}
--- FIM DO CONTEXTO ---"""


def gerar_simulado(
    turma_id: str,
    disciplina: str,
    topico: str = "todo o conteúdo disponível",
    n_questoes: int = 5,
) -> dict:
    """
    Gera um simulado de múltipla escolha com base nos materiais de
    História ou Geografia já liberados para a turma.
    """
    contexto_recuperado = recuperar_contexto(
        pergunta=topico,
        turma_id=turma_id,
        disciplina=disciplina,
        n_resultados=10,
    )

    if not contexto_recuperado.trechos:
        return {
            "erro": (
                f"Nenhum material de {disciplina.capitalize()} "
                "disponível para esta turma até o momento."
            )
        }

    contexto = "\n\n---\n\n".join(contexto_recuperado.trechos)
    prompt = PROMPT_SIMULADO.format(
        disciplina=disciplina.capitalize(),
        n_questoes=n_questoes,
        contexto=contexto,
    )

    client = get_active_gemini_client()
    resposta = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config={"temperature": 0.3, "response_mime_type": "application/json"},
    )

    return json.loads(resposta.text)
```


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🛣️ Rotas da API (FastAPI)

| Método | Rota | Perfil | Descrição |
| ------ | ---- | ------ | --------- |
| `POST` | `/auth/register` | Público | Cadastro de usuário |
| `POST` | `/auth/login` | Público | Login + geração de JWT |
| `GET` | `/turmas` | Professor | Lista turmas do professor autenticado |
| `POST` | `/turmas` | Professor | Cria nova turma |
| `POST` | `/turmas/{id}/materiais` | Professor | Upload de PDF com disciplina e data de liberação |
| `GET` | `/turmas/{id}/alunos` | Professor | Lista alunos matriculados na turma |
| `POST` | `/aluno/turmas/{id}/ingressar` | Aluno | Aluno ingressa em uma turma |
| `POST` | `/chat/mensagem` | Aluno | Envia pergunta ao tutor RAG (História ou Geografia) |
| `GET` | `/chat/historico` | Aluno | Histórico de conversas do aluno |
| `POST` | `/simulado/gerar` | Aluno | Gera quiz com o conteúdo liberado |
| `POST` | `/simulado/{id}/responder` | Aluno | Submete respostas e calcula pontuação |


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🚀 Guia Completo de Instalação (Passo a Passo)

Este guia assume que você está começando do zero, sem nada instalado. Segue exatamente na ordem.

### 1. Pré-requisitos (o que baixar)

Instale cada item abaixo e confirme a versão pelo terminal.

| Ferramenta | Versão mínima | Download | Comando de verificação |
| ---------- | -------------- | -------- | ----------------------- |
| **Git** | qualquer recente | [git-scm.com/downloads](https://git-scm.com/downloads) | `git --version` |
| **Python** | 3.11+ | [python.org/downloads](https://www.python.org/downloads/) | `python3 --version` |
| **Node.js** | 18+ (LTS) | [nodejs.org](https://nodejs.org/) | `node --version` e `npm --version` |
| **PostgreSQL** | 16+ | [postgresql.org/download](https://www.postgresql.org/download/) | `psql --version` |
| **Extensão pgvector** | compatível com seu PG | [github.com/pgvector/pgvector](https://github.com/pgvector/pgvector#installation) | ver passo 3 |
| **Chave de API Gemini** | — | [ai.google.dev](https://ai.google.dev) → "Get API key" | — |

> 💡 No Linux (Ubuntu/Mint), Python e Git geralmente já vêm instalados ou disponíveis via `apt`. No Windows, use os instaladores oficiais e marque a opção "Add to PATH".

**Instalando pré-requisitos no Linux (Ubuntu/Mint):**

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip postgresql postgresql-contrib build-essential

# Node.js via nvm (recomendado, evita conflito de versões)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts
```

**Instalando pré-requisitos no macOS (via Homebrew):**

```bash
brew install git python@3.11 node postgresql@16
brew services start postgresql@16
```

**Instalando pré-requisitos no Windows:**

1. Baixe e instale o [Git for Windows](https://git-scm.com/download/win)
2. Baixe e instale o [Python 3.11+](https://www.python.org/downloads/windows/) (marque "Add Python to PATH")
3. Baixe e instale o [Node.js LTS](https://nodejs.org/)
4. Baixe e instale o [PostgreSQL 16](https://www.postgresql.org/download/windows/) usando o instalador oficial (inclui o pgAdmin)

---

### 2. Clonar o repositório

```bash
git clone https://github.com/KaroliniRPedrozo/ChronosBot.git
cd ChronosBot
```

---

### 3. Configurar o PostgreSQL + pgvector

**3.1. Crie o banco de dados:**

```bash
# Acesse o psql como superusuário
sudo -u postgres psql        # Linux
psql -U postgres             # macOS/Windows
```

Dentro do `psql`:

```sql
CREATE DATABASE chronosbot;
CREATE USER chronosbot_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE chronosbot TO chronosbot_user;
\q
```

**3.2. Instale a extensão `pgvector`:**

```bash
# Ubuntu/Mint — instala o pacote correspondente à sua versão do Postgres
sudo apt install postgresql-16-pgvector

# macOS (Homebrew)
brew install pgvector

# Caso o pacote não exista para sua versão, compile do source:
git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
cd ..
```

**3.3. Habilite a extensão dentro do banco criado:**

```bash
psql -U chronosbot_user -d chronosbot -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

### 4. Configurar o Backend

**4.1. Crie e ative o ambiente virtual Python:**

```bash
python3 -m venv .venv

# Ativar no Linux/macOS
source .venv/bin/activate

# Ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Ativar no Windows (cmd)
.venv\Scripts\activate.bat
```

> Você saberá que ativou corretamente quando o terminal mostrar `(.venv)` no início da linha.

**4.2. Instale as dependências:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4.3. Configure as variáveis de ambiente:**

```bash
cp .env.example .env
```

Abra o arquivo `.env` (com `nano .env`, VS Code, etc.) e preencha:

```env
DATABASE_URL=postgresql://chronosbot_user:sua_senha_aqui@localhost:5432/chronosbot
GEMINI_API_KEYS=AIza...,AIza...,AIza...   # uma ou mais chaves separadas por vírgula
JWT_SECRET=gere-uma-chave-aleatoria-aqui
JWT_EXPIRE_MINUTES=1440
```

> Para gerar um `JWT_SECRET` seguro: `python3 -c "import secrets; print(secrets.token_hex(32))"`

**4.4. Rode as migrações / inicialize as tabelas:**

```bash
python -m scripts.init_db
```

---

### 5. Configurar o Frontend

Em um **novo terminal** (mantenha o backend/venv do passo anterior aberto em outro):

```bash
cd ChronosBot/frontend
npm install
```

Se o frontend também usar variáveis de ambiente (ex: URL da API), copie o exemplo:

```bash
cp .env.example .env.local
# Edite .env.local, geralmente algo como:
# VITE_API_URL=http://localhost:8000
```

---

### 6. Rodar o projeto

Você vai precisar de **dois terminais abertos ao mesmo tempo**:

```bash
# Terminal 1 — Backend (dentro da pasta raiz do projeto, com .venv ativado)
uvicorn main:app --reload
# Backend disponível em http://localhost:8000
# Docs interativas (Swagger) em http://localhost:8000/docs
```

```bash
# Terminal 2 — Frontend
cd frontend
npm run dev
# Frontend disponível em http://localhost:5173 (padrão Vite)
```

---

### 7. Verificação final

- [ ] `http://localhost:8000/docs` abre a documentação Swagger da API
- [ ] `http://localhost:5173` (ou porta indicada pelo `npm run dev`) abre a interface do ChronosBot
- [ ] Consegue criar um usuário via `/auth/register` e logar via `/auth/login`
- [ ] `psql -U chronosbot_user -d chronosbot -c "\dx"` lista `vector` entre as extensões instaladas

---

### ⚠️ Problemas comuns

| Erro | Causa provável | Solução |
| ---- | --------------- | ------- |
| `extension "vector" is not available` | pgvector não instalado/compilado para a versão do Postgres | Repita o passo 3.2 conferindo a versão exata do Postgres (`psql --version`) |
| `password authentication failed for user` | Usuário/senha do `.env` não bate com o criado no passo 3.1 | Confira `DATABASE_URL` e a senha criada no `CREATE USER` |
| `ModuleNotFoundError` ao rodar `uvicorn` | Ambiente virtual não ativado ou dependência faltando | Ative o `.venv` e rode `pip install -r requirements.txt` novamente |
| `429 Too Many Requests` do Gemini | Cota do free tier estourada | Adicione mais chaves em `GEMINI_API_KEYS` (separadas por vírgula) para ativar a rotação |
| Frontend não conecta no backend (erro de CORS) | URL da API errada ou CORS não configurado | Confira `VITE_API_URL` no `.env.local` e as origens permitidas no CORS do FastAPI |
| `npm install` falha com erros de permissão | Node instalado via método que exige `sudo` | Reinstale o Node via `nvm` (ver passo 1) para evitar precisar de `sudo` |


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🗂️ Estrutura do Projeto

```text
ChronosBot/
├── backend/
│   ├── main.py                   ← Entrypoint FastAPI
│   ├── auth/                     ← JWT + RBAC
│   ├── routes/                   ← chat.py, turmas.py, simulado.py
│   ├── rag/
│   │   ├── retriever.py          ← Busca vetorial (pgvector) com filtros
│   │   ├── indexer.py            ← Indexação de PDFs (pypdf) na base
│   │   ├── key_rotation.py       ← Rotação de chaves Gemini
│   │   └── simulado.py           ← Geração de quiz via Gemini
│   ├── models/                   ← SQLAlchemy ORM + schemas Pydantic v2
│   └── database.py               ← Conexão PostgreSQL
├── frontend/
│   ├── src/
│   │   ├── assets/                ← logo.png e demais imagens
│   │   ├── components/            ← componentes React
│   │   └── pages/                 ← telas React (chat, simulado, professor)
│   └── legacy/                    ← páginas HTML/JS em processo de migração
├── scripts/
│   └── init_db.py
├── requirements.txt
├── .env.example
└── README.md
```


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🔒 Segurança e Conformidade

- **Autenticação:** JWT com expiração configurável e refresh token
- **RBAC:** Middleware que impede alunos de acessar rotas administrativas do professor
- **Escopo Disciplinar:** O motor RAG filtra ativamente perguntas fora de História e Geografia
- **LGPD:** Logs anonimizados, sem armazenamento de conteúdo pessoal em texto livre
- **Filtro RAG:** A IA **nunca** acessa conteúdo de outra turma ou anterior à data de liberação
- **Chaves de API:** gerenciadas via pool com rotação automática; nunca versionadas no repositório


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 📊 Métricas de Qualidade (ISO/IEC 25010)

| Atributo | Indicador | Meta |
| -------- | --------- | ---- |
| Eficiência de Desempenho | Latência mediana do chat | < 2.000 ms |
| Confiabilidade | Disponibilidade do serviço (uptime) | > 99,5% |
| Usabilidade | Taxa de abandono de sessão | < 15% |
| Funcionalidade | Cobertura de queries respondidas com contexto | ≥ 80% |
| Segurança | Tentativas de acesso não autorizado bloqueadas | 100% |


<p align="right">(<a href="#topo">voltar ao topo</a>)</p>

---

## 🤝 Contribuindo

Contribuições são bem-vindas. Para reportar bugs ou propor melhorias, abra uma *issue* detalhando o contexto. Para contribuição de código, envie um *pull request* com descrição clara das alterações realizadas.

---

<p align="center">
  Desenvolvido como Trabalho de Conclusão de Curso (TCC) · 2025<br>
  <a href="https://github.com/KaroliniRPedrozo">@KaroliniRPedrozo</a>
</p>