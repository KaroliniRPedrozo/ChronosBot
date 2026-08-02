# ChronosBot

<h1 align="center">
  <img src="https://github.com/KaroliniRPedrozo/ChronosBot/blob/main/frontend/assets/logo.png" width="100" alt="ChronosBot Logo"><br>
  ChronosBot
</h1>

**Plataforma de tutoria inteligente com RAG — onde professores ensinam a IA e a IA ensina os alunos.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-FF6B35?style=flat-square)](https://trychroma.com)
[![Gemini](https://img.shields.io/badge/Gemini-API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)

---

## 📊 Status de Desenvolvimento

| Módulo | Status | Progresso |
| ------ | ------ | --------- |
| 🗄️ Banco de Dados (Modelos & Esquema) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🔐 Autenticação (JWT / RBAC) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🧠 Motor RAG (Indexação & Retrieval) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 📝 Modo Simulado (Quiz) | ✅ Concluído | ![100%](https://img.shields.io/badge/100%25-brightgreen?style=flat-square) |
| 🛣️ Rotas do Professor | 🔄 Em andamento | ![70%](https://img.shields.io/badge/70%25-yellow?style=flat-square) |
| 🛣️ Rotas do Aluno | 🔄 Em andamento | ![60%](https://img.shields.io/badge/60%25-yellow?style=flat-square) |
| ⚙️ Backend (Integração Geral) | 🔄 Em andamento | ![75%](https://img.shields.io/badge/75%25-yellow?style=flat-square) |
| 🌐 Frontend (Interface Web) | 🔄 Em andamento | ![40%](https://img.shields.io/badge/40%25-orange?style=flat-square) |
| 🧪 Testes & Validação | ⏳ Pendente | ![0%](https://img.shields.io/badge/0%25-lightgrey?style=flat-square) |

> **Versão atual:** `0.7-beta` · **Última atualização:** Julho/2025

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

---

## 🏗️ Arquitetura do Sistema

```text
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│        HTML + CSS + JavaScript (Fetch API / SSE)            │
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
┌─────────────────────┐              ┌──────────────────────────┐
│  ChromaDB (Vetorial)│              │  Google Gemini API       │
│  embeddings + meta  │              │  (LLM Generativo)        │
└─────────────────────┘              └──────────────────────────┘
          │
┌─────────▼───────────────┐
│  PostgreSQL (Relacional)│
│  users, turmas,         │
│  arquivos, permissões   │
└─────────────────────────┘
```

---

## 🗄️ Esquema do Banco de Dados Relacional

```sql
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

O banco vetorial **ChromaDB** armazena os embeddings com metadados que espelham a tabela `arquivos`:

```python
# Metadados armazenados em cada chunk do ChromaDB
{
    "arquivo_id":     "uuid-do-arquivo",
    "turma_id":       "uuid-da-turma",
    "disciplina":     "historia",       # "historia" | "geografia"
    "data_liberacao": "2025-08-01"      # string ISO para filtro temporal
}
```

---

## 🧠 Lógica RAG com Filtro Temporal (Python)

A recuperação de documentos aplica **dois filtros obrigatórios** antes de qualquer consulta ao LLM: o vínculo da turma e a data de liberação. Isso garante que a IA nunca acesse conteúdo de outra turma ou de datas futuras.

```python
# rag/retriever.py
from datetime import date
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

# Configuração do cliente ChromaDB e função de embedding via Gemini
chroma_client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)

# Usando o modelo de embeddings do Google
class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __call__(self, input: list[str]) -> list[list[float]]:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=input,
            task_type="retrieval_document"
        )
        return result["embedding"] if isinstance(input, str) else result["embedding"]

collection = chroma_client.get_collection(
    name="materiais_educacionais",
    embedding_function=GeminiEmbeddingFunction()
)

DISCIPLINAS_PERMITIDAS = {"historia", "geografia"}

def recuperar_contexto(
    pergunta: str,
    turma_id: str,
    disciplina: str,
    n_resultados: int = 5
) -> list[str]:
    """
    Recupera chunks relevantes APENAS dos materiais de História ou Geografia
    vinculados à turma do aluno e já liberados até a data atual.

    Args:
        pergunta:     Texto da dúvida do aluno.
        turma_id:     UUID da turma à qual o aluno pertence.
        disciplina:   "historia" ou "geografia".
        n_resultados: Número de chunks a recuperar.

    Returns:
        Lista de strings com os trechos relevantes encontrados.

    Raises:
        ValueError: Se a disciplina solicitada não for suportada.
    """
    if disciplina not in DISCIPLINAS_PERMITIDAS:
        raise ValueError(
            f"Disciplina '{disciplina}' não suportada. "
            f"Opções válidas: {DISCIPLINAS_PERMITIDAS}"
        )

    hoje = date.today().isoformat()  # ex: "2025-07-08"

    resultados = collection.query(
        query_texts=[pergunta],
        n_results=n_resultados,
        where={
            "$and": [
                {"turma_id":        {"$eq": turma_id}},
                {"disciplina":      {"$eq": disciplina}},
                {"data_liberacao":  {"$lte": hoje}}
            ]
        },
        include=["documents", "distances"]
    )

    documentos = resultados.get("documents", [[]])[0]
    return documentos  # lista de strings (chunks)
```

---

## 📝 Modo Simulado (Geração de Quiz com Gemini)

```python
# rag/simulado.py
import json
import google.generativeai as genai
from .retriever import recuperar_contexto

genai.configure(api_key=settings.GEMINI_API_KEY)
modelo_gemini = genai.GenerativeModel("gemini-1.5-flash")

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
    n_questoes: int = 5
) -> dict:
    """
    Gera um simulado de múltipla escolha com base nos materiais de
    História ou Geografia já liberados para a turma.

    Args:
        turma_id:   UUID da turma.
        disciplina: "historia" ou "geografia".
        topico:     Tema específico para filtrar a busca (opcional).
        n_questoes: Quantidade de questões a gerar (padrão: 5).

    Returns:
        Dicionário com a lista de questões, gabaritos e justificativas.
    """
    chunks = recuperar_contexto(
        pergunta=topico,
        turma_id=turma_id,
        disciplina=disciplina,
        n_resultados=10
    )

    if not chunks:
        return {
            "erro": (
                f"Nenhum material de {disciplina.capitalize()} "
                "disponível para esta turma até o momento."
            )
        }

    contexto = "\n\n---\n\n".join(chunks)
    prompt   = PROMPT_SIMULADO.format(
        disciplina=disciplina.capitalize(),
        n_questoes=n_questoes,
        contexto=contexto
    )

    resposta = modelo_gemini.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json"
        )
    )

    return json.loads(resposta.text)
```

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

### Exemplo de rota de chat com filtro RAG e Gemini

```python
# routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..auth import get_current_user
from ..rag.retriever import recuperar_contexto, DISCIPLINAS_PERMITIDAS
import google.generativeai as genai

router = APIRouter(prefix="/chat", tags=["Chat Tutor"])
genai.configure(api_key=settings.GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

class MensagemPayload(BaseModel):
    mensagem:   str
    disciplina: str  # "historia" | "geografia"

@router.post("/mensagem")
async def enviar_mensagem(
    payload: MensagemPayload,
    usuario = Depends(get_current_user)
):
    # Valida se a disciplina é suportada pelo sistema
    if payload.disciplina not in DISCIPLINAS_PERMITIDAS:
        raise HTTPException(
            status_code=422,
            detail=(
                "O ChronosBot atende apenas às disciplinas de "
                "História e Geografia."
            )
        )

    turma_id = usuario.turma_id  # extraído do JWT do aluno autenticado

    # 1. Recupera contexto com filtro de turma + disciplina + data
    chunks   = recuperar_contexto(
        pergunta=payload.mensagem,
        turma_id=turma_id,
        disciplina=payload.disciplina
    )
    contexto = "\n\n".join(chunks) if chunks else ""

    # 2. Monta prompt com guardrail pedagógico e escopo disciplinar
    system_prompt = f"""Você é o ChronosBot, um tutor educacional especializado
em {payload.disciplina.capitalize()} para a Educação Básica.

Diretrizes obrigatórias:
- Responda SOMENTE com base no contexto fornecido abaixo
- Caso a resposta não esteja no contexto, informe:
  'Este conteúdo ainda não foi liberado para sua turma.'
- Caso a pergunta seja de outra disciplina, informe:
  'Só posso auxiliar com questões de História e Geografia.'
- Nunca invente ou extrapole informações além do contexto
- Use linguagem clara e adequada ao nível do Ensino Básico

CONTEXTO:
{contexto}"""

    # 3. Gera resposta via Gemini
    resposta = modelo.generate_content(
        [system_prompt, payload.mensagem],
        generation_config=genai.GenerationConfig(temperature=0.2)
    )

    return {"resposta": resposta.text}
```

---

## 🚀 Como Rodar Localmente

### Pré-requisitos

- Python 3.11+
- PostgreSQL 16
- Docker (para o ChromaDB)
- Chave de API do Google Gemini ([obter aqui](https://ai.google.dev))

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/KaroliniRPedrozo/ChronosBot.git
cd ChronosBot

# 2. Crie o ambiente virtual e instale as dependências
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# 4. Suba o ChromaDB com Docker
docker run -d -p 8000:8000 chromadb/chroma

# 5. Inicialize as tabelas no PostgreSQL
python -m scripts.init_db

# 6. Inicie o servidor de desenvolvimento
uvicorn main:app --reload
```

### Variáveis de Ambiente (`.env`)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/chronosbot
GEMINI_API_KEY=AIza...
CHROMA_HOST=localhost
CHROMA_PORT=8000
JWT_SECRET=sua-chave-secreta-aqui
JWT_EXPIRE_MINUTES=1440
```

---

## 🗂️ Estrutura do Projeto

```text
ChronosBot/
├── assets/
│   └── logo.png                  ← Logotipo do projeto
├── backend/
│   ├── main.py                   ← Entrypoint FastAPI
│   ├── auth/                     ← JWT + RBAC
│   ├── routes/                   ← chat.py, turmas.py, simulado.py
│   ├── rag/
│   │   ├── retriever.py          ← Busca vetorial com filtros (turma + disciplina + data)
│   │   ├── indexer.py            ← Indexação de PDFs no ChromaDB
│   │   └── simulado.py           ← Geração de quiz via Gemini
│   ├── models/                   ← SQLAlchemy ORM
│   └── database.py               ← Conexão PostgreSQL
├── frontend/
│   ├── index.html
│   ├── chat.html
│   ├── simulado.html
│   ├── professor/
│   └── js/
│       ├── api.js                ← Fetch wrapper com JWT
│       └── chat.js
├── scripts/
│   └── init_db.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔒 Segurança e Conformidade

- **Autenticação:** JWT com expiração configurável e refresh token
- **RBAC:** Middleware que impede alunos de acessar rotas administrativas do professor
- **Escopo Disciplinar:** O motor RAG filtra ativamente perguntas fora de História e Geografia
- **LGPD:** Logs anonimizados, sem armazenamento de conteúdo pessoal em texto livre
- **Filtro RAG:** A IA **nunca** acessa conteúdo de outra turma ou anterior à data de liberação

---

## 📊 Métricas de Qualidade (ISO/IEC 25010)

| Atributo | Indicador | Meta |
| -------- | --------- | ---- |
| Eficiência de Desempenho | Latência mediana do chat | < 2.000 ms |
| Confiabilidade | Disponibilidade do serviço (uptime) | > 99,5% |
| Usabilidade | Taxa de abandono de sessão | < 15% |
| Funcionalidade | Cobertura de queries respondidas com contexto | ≥ 80% |
| Segurança | Tentativas de acesso não autorizado bloqueadas | 100% |

---

## 🤝 Contribuindo

Contribuições são bem-vindas. Para reportar bugs ou propor melhorias, abra uma *issue* detalhando o contexto. Para contribuição de código, envie um *pull request* com descrição clara das alterações realizadas.

---

<p align="center">
  Desenvolvido como Trabalho de Conclusão de Curso (TCC) · 2025<br>
  <a href="https://github.com/KaroliniRPedrozo">@KaroliniRPedrozo</a>
</p>
