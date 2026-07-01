<div align="center">

# 🕰️ ChronosBot

### Plataforma Educacional de Tutoria Inteligente com Arquitetura RAG

*Um chatbot educacional onde professores disponibilizam materiais de aula por turma, permitindo que alunos cadastrados tirem dúvidas e realizem simulados com base estrita no conteúdo já liberado.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)](https://www.trychroma.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](#licença)

</div>

---

## 📖 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [A Regra de Ouro do Sistema](#-a-regra-de-ouro-do-sistema)
- [Arquitetura](#-arquitetura)
- [Stack Tecnológica](#-stack-tecnológica)
- [Modelo de Dados](#-modelo-de-dados)
- [Pipeline RAG](#-pipeline-rag)
- [Perfis de Usuário e Funcionalidades](#-perfis-de-usuário-e-funcionalidades)
- [Estrutura de Rotas da API](#-estrutura-de-rotas-da-api)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Instalação e Execução](#-instalação-e-execução)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#licença)

---

## Sobre o Projeto

O **ChronosBot** é uma plataforma full-stack de tutoria educacional baseada em **Geração Aumentada por Recuperação (RAG)**. O sistema foi desenhado para resolver um problema comum em ambientes de ensino mediados por IA: como garantir que um chatbot educacional **nunca "vaze" conteúdo futuro** ou fora do escopo curricular liberado pelo professor.

Diferente de chatbots educacionais genéricos, o ChronosBot trata o controle de acesso ao conhecimento como uma **regra de negócio arquitetural**, não como uma instrução de prompt — a IA fisicamente não tem acesso aos embeddings de materiais ainda não liberados para a turma do aluno.

O projeto nasce em contexto acadêmico, aplicando conceitos de:
- Engenharia de Software (arquitetura em camadas, separação de responsabilidades)
- Segurança da Informação (autenticação, autorização e minimização de dados)
- Engenharia de IA Generativa (RAG, prompt engineering, structured outputs)

---

## 🔐 A Regra de Ouro do Sistema

> **A IA só pode consultar materiais que já foram explicitamente liberados para a turma daquele aluno, em uma data igual ou anterior à data atual.**

Essa regra é **enforçada na camada de recuperação de dados (retrieval layer)**, nunca delegada ao modelo de linguagem. O fluxo de decisão nunca pergunta à IA "isso é permitido?" — a IA simplesmente nunca recebe, no seu contexto, nada que não devesse ver.

```
┌─────────────────────────────────────────────────────────────┐
│  1️⃣  Consulta relacional (PostgreSQL)                        │
│      → Quais materiais estão liberados para esta turma       │
│        HOJE, segundo a tabela MaterialTurmaPermissao?        │
│                                                                │
│  2️⃣  Busca vetorial filtrada (ChromaDB)                      │
│      → Buscar embeddings SOMENTE dentro do conjunto           │
│        de material_id retornado na etapa 1                   │
│                                                                │
│  3️⃣  Geração (LLM)                                           │
│      → A IA responde usando apenas o contexto recuperado      │
└─────────────────────────────────────────────────────────────┘
```

Essa é a peça central do design: **decoupling entre a existência de um material e sua liberação por turma**, via a tabela pivô `MaterialTurmaPermissao`.

---

## 🏗️ Arquitetura

```
                              ┌──────────────────────┐
                              │      Frontend         │
                              │  (React / HTML+JS)    │
                              └──────────┬────────────┘
                                         │ HTTPS / JWT Bearer Token
                                         ▼
                              ┌──────────────────────┐
                              │   FastAPI Backend     │
                              │  ┌────────────────┐  │
                              │  │  routes_auth    │  │
                              │  │  routes_professor│  │
                              │  │  routes_aluno   │  │
                              │  └────────────────┘  │
                              └───┬──────────────┬───┘
                                  │              │
                    ┌─────────────▼───┐   ┌─────▼──────────────┐
                    │  PostgreSQL      │   │  ChromaDB           │
                    │  (SQLAlchemy)    │   │  (Vector Store)      │
                    │                  │   │                     │
                    │  Regras de       │   │  Embeddings dos      │
                    │  negócio,        │   │  materiais didáticos │
                    │  permissões,     │   │  + metadata          │
                    │  usuários        │   │  (material_id,       │
                    └──────────────────┘   │   turma_id)          │
                                            └─────────┬───────────┘
                                                       │
                                            ┌──────────▼───────────┐
                                            │   OpenAI API          │
                                            │  (Chat + Embeddings)  │
                                            └───────────────────────┘
```

**Princípio arquitetural central:** o banco relacional é a **fonte da verdade sobre permissões**; o banco vetorial é a **fonte da verdade sobre conteúdo semântico**. Toda consulta passa primeiro pelo relacional para resolver a lista de IDs permitidos, e só então toca o vetorial — nunca o inverso.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Finalidade |
|---|---|---|
| **Backend** | Python 3.11+ / FastAPI | API REST, lógica de negócio, validação |
| **ORM** | SQLAlchemy | Mapeamento objeto-relacional |
| **Banco Relacional** | PostgreSQL (prod) / SQLite (dev) | Usuários, turmas, permissões, metadados |
| **Banco Vetorial** | ChromaDB | Armazenamento de embeddings dos materiais |
| **IA Generativa** | OpenAI API (Chat Completions + Embeddings) | Tutoria conversacional e geração de simulados |
| **Autenticação** | JWT + bcrypt | Identidade extraída do token, nunca do body |
| **Validação** | Pydantic | Schemas de entrada/saída da API |
| **Frontend** | React (ou HTML/CSS/JS vanilla) | Interface do professor e do aluno |
| **Processamento de Documentos** | LangChain / PyPDF | Ingestão, chunking e indexação de PDFs |

---

## 🗄️ Modelo de Dados

### Esquema Relacional

```
┌────────────────┐        ┌────────────────┐        ┌────────────────┐
│   Professor     │        │     Turma       │        │     Aluno       │
├────────────────┤        ├────────────────┤        ├────────────────┤
│ id (PK)         │───┐    │ id (PK)         │    ┌──►│ id (PK)         │
│ nome            │   │    │ nome            │    │   │ nome            │
│ email           │   │    │ ano_letivo      │    │   │ email           │
│ senha_hash      │   └───►│ professor_id(FK)│◄───┘   │ senha_hash      │
│ criado_em       │        │ criado_em       │        │ turma_id (FK)   │
└────────────────┘        └───────┬────────┘        │ criado_em       │
                                   │                  └────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Material                │
                    ├──────────────────────────────┤
                    │ id (PK)                       │
                    │ titulo                        │
                    │ nome_arquivo                  │
                    │ professor_id (FK)              │
                    │ vector_collection_id            │
                    │ criado_em                      │
                    └──────────────┬────────────────┘
                                   │
                    ┌──────────────▼────────────────────┐
                    │     MaterialTurmaPermissao         │  ★ Tabela pivô
                    ├────────────────────────────────────┤     (o coração
                    │ id (PK)                            │      do controle
                    │ material_id (FK)                   │      de acesso)
                    │ turma_id (FK)                       │
                    │ data_liberacao      ◄──── regra     │
                    │ liberado_por (FK → Professor)       │
                    │ criado_em                           │
                    └────────────────────────────────────┘
```

### Por que uma tabela pivô e não um campo direto em `Material`?

Um material pode ser reaproveitado por **múltiplas turmas**, cada uma com sua **própria data de liberação** (ex.: o mesmo PDF de "Frações" pode ser liberado para o 6º Ano A em março e para o 6º Ano B em abril). Se a data de liberação fosse um campo em `Material`, seria impossível reutilizar o mesmo arquivo com cronogramas distintos por turma — e o professor teria que duplicar arquivos desnecessariamente. A tabela `MaterialTurmaPermissao` resolve isso como uma relação N:N com atributo (a data), que é o padrão correto para esse tipo de regra de negócio.

### Conexão com o Banco Vetorial

O ChromaDB não guarda regras de negócio — ele guarda **chunks de texto vetorizados**, cada um com metadados mínimos que permitem filtrar:

```python
{
    "material_id": "mat_048f3a",
    "chunk_index": 12,
    "source_filename": "fracoes_6ano.pdf"
}
```

O `turma_id` e a `data_liberacao` **não** vivem no metadata do vetor — eles vivem exclusivamente no PostgreSQL. Isso é intencional: manter a regra de acesso em um único lugar (o relacional) evita duplicação de estado e inconsistências entre os dois bancos.

---

## 🔍 Pipeline RAG

A recuperação de contexto segue um fluxo de **duas etapas obrigatórias**:

```python
from datetime import date
from sqlalchemy.orm import Session
import chromadb

def buscar_material_ids_permitidos(db: Session, turma_id: int) -> list[str]:
    """
    ETAPA 1 — Relacional
    Resolve quais materiais estão liberados para a turma HOJE.
    Esta é a única fonte da verdade sobre permissão de acesso.
    """
    permissoes = (
        db.query(MaterialTurmaPermissao.material_id)
        .filter(
            MaterialTurmaPermissao.turma_id == turma_id,
            MaterialTurmaPermissao.data_liberacao <= date.today(),
        )
        .all()
    )
    return [str(p.material_id) for p in permissoes]


def recuperar_contexto(
    pergunta: str,
    turma_id: int,
    db: Session,
    chroma_client: chromadb.Client,
    top_k: int = 5,
) -> list[str]:
    """
    ETAPA 2 — Vetorial filtrada
    Busca semântica restrita ao conjunto de material_id permitido.
    Se a lista vier vazia, retorna vazio SEM consultar o vetorial —
    não há necessidade de gastar uma chamada de busca se não há
    nada que o aluno possa ver.
    """
    material_ids_permitidos = buscar_material_ids_permitidos(db, turma_id)

    if not material_ids_permitidos:
        return []

    collection = chroma_client.get_collection("materiais_didaticos")

    resultados = collection.query(
        query_texts=[pergunta],
        n_results=top_k,
        where={"material_id": {"$in": material_ids_permitidos}},  # 🔒 filtro obrigatório
    )

    return resultados["documents"][0] if resultados["documents"] else []
```

> ⚠️ **Nunca** construa a query vetorial sem o `where`. Uma busca vetorial sem esse filtro é, por definição, uma falha de segurança — não um bug cosmético.

---

## 📝 Modo Simulado

O simulado usa o mesmo pipeline de recuperação (com um `top_k` mais amplo, para cobrir múltiplos tópicos), mas troca o prompt de "tutor" por um prompt de "examinador", forçando saída estruturada em JSON:

```python
import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT_SIMULADO = """\
Você é um examinador educacional. Sua única função é gerar questões de \
múltipla escolha (4 alternativas, 1 correta) EXCLUSIVAMENTE com base no \
CONTEXTO fornecido abaixo. Você não pode usar conhecimento externo ao \
contexto, mesmo que o conheça.

Se o contexto for insuficiente para gerar o número de questões pedido, \
gere o máximo possível e informe a limitação no campo "observacao".

Responda SOMENTE em JSON válido, sem markdown, sem texto antes ou depois, \
seguindo exatamente este formato:
{
  "questoes": [
    {
      "enunciado": "string",
      "alternativas": {"A": "string", "B": "string", "C": "string", "D": "string"},
      "resposta_correta": "A",
      "material_referencia": "string (título do material de origem)"
    }
  ],
  "observacao": "string ou null"
}
"""

def gerar_simulado(pergunta_tema: str, contexto: list[str], num_questoes: int = 5) -> dict:
    contexto_formatado = "\n\n---\n\n".join(contexto)

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_SIMULADO},
            {
                "role": "user",
                "content": (
                    f"CONTEXTO:\n{contexto_formatado}\n\n"
                    f"Gere {num_questoes} questões sobre: {pergunta_tema}"
                ),
            },
        ],
    )

    return json.loads(resposta.choices[0].message.content)
```

O `contexto` passado a essa função **já passou** pelo filtro relacional + vetorial descrito na seção anterior — o simulado herda automaticamente a mesma garantia de que não escapa conteúdo não liberado.

---

## 👥 Perfis de Usuário e Funcionalidades

### 🧑‍🏫 Professor (Admin de Conteúdo)

| Funcionalidade | Descrição |
|---|---|
| Gestão de turmas | Criar e listar turmas (ex.: "6º Ano A") |
| Upload de materiais | Envio de PDFs/textos; disparo do pipeline de ingestão RAG |
| Controle de liberação | Vincular material → turma(s) com data de liberação individual |
| Painel de acompanhamento | Visualizar quais materiais estão ativos por turma |

### 🎓 Aluno (Usuário Final)

| Funcionalidade | Descrição |
|---|---|
| Cadastro e vínculo | Conta própria, associada a uma turma no momento do cadastro |
| Chat com tutor IA | Perguntas respondidas com base estrita no material liberado |
| Modo Simulado | Geração de quiz de múltipla escolha sobre o conteúdo já estudado |
| Histórico de sessão | Consulta de interações anteriores com o tutor |

---

## 🌐 Estrutura de Rotas da API

| Método | Rota | Perfil | Descrição |
|---|---|---|---|
| `POST` | `/auth/register/professor` | Público | Cadastro de professor |
| `POST` | `/auth/register/aluno` | Público | Cadastro de aluno (com seleção de turma) |
| `POST` | `/auth/login` | Público | Login unificado, retorna JWT |
| `POST` | `/professor/turmas` | Professor | Cria nova turma |
| `GET` | `/professor/turmas` | Professor | Lista turmas do professor logado |
| `POST` | `/professor/materiais` | Professor | Upload de arquivo + disparo de ingestão RAG |
| `POST` | `/professor/materiais/{id}/liberar` | Professor | Vincula material a turma(s) com data de liberação |
| `GET` | `/professor/materiais` | Professor | Lista materiais e status de liberação |
| `GET` | `/aluno/materiais-disponiveis` | Aluno | Lista o que já está liberado para a turma do aluno |
| `POST` | `/aluno/chat` | Aluno | Envia pergunta ao tutor IA |
| `POST` | `/aluno/simulado` | Aluno | Gera simulado com base no material liberado |
| `GET` | `/aluno/historico` | Aluno | Retorna histórico de conversas |

> 🔒 Em todas as rotas de `/professor/*` e `/aluno/*`, a identidade (e por consequência a turma, no caso do aluno) é extraída do **token JWT decodificado no backend** via dependência do FastAPI — nunca de um campo enviado no corpo da requisição pelo frontend. Isso impede que um aluno manipule a requisição para se passar por integrante de outra turma.

### Como o Frontend Consome essas Rotas com Segurança

```javascript
// Exemplo: frontend enviando pergunta ao tutor
const resposta = await fetch("/aluno/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${tokenJWT}`, // turma_id NUNCA vai no body
  },
  body: JSON.stringify({ pergunta: "O que é uma fração equivalente?" }),
});
```

O backend decodifica o token, extrai `aluno_id` → resolve `turma_id` no banco → só então executa o pipeline RAG. O frontend nunca decide, nunca informa e nunca deveria saber a `turma_id` de forma autoritativa — ele apenas exibe o que o backend retorna.

---

## 📂 Estrutura de Pastas

```
ChronosBot/
├── backend/
│   ├── app/
│   │   ├── database.py          # Engine e sessão SQLAlchemy
│   │   ├── models.py             # Schema relacional (inclui MaterialTurmaPermissao)
│   │   ├── schemas.py            # Modelos Pydantic (request/response)
│   │   ├── auth.py               # Hash bcrypt, JWT, dependências de identidade
│   │   ├── rag.py                # Ingestão de PDFs, chunking, embeddings, retrieval
│   │   ├── simulado.py           # Geração de quiz via LLM
│   │   ├── routes_auth.py        # Rotas de registro/login
│   │   ├── routes_professor.py   # Rotas exclusivas do professor
│   │   ├── routes_aluno.py       # Rotas exclusivas do aluno
│   │   └── main.py               # Ponto de entrada FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
│   └── (documentação acadêmica / dissertação de referência)
└── README.md
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11+
- Node.js 18+ (se o frontend for React)
- PostgreSQL 14+ (ou SQLite para desenvolvimento local)
- Chave de API da OpenAI

### Backend

```bash
# Clone o repositório
git clone https://github.com/KaroliniRPedrozo/ChronosBot.git
cd ChronosBot/backend

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependências
pip install -r requirements.txt

# Variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# Execução
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`, com documentação interativa automática em `http://localhost:8000/docs` (Swagger UI).

### Frontend

```bash
cd ChronosBot/frontend
npm install
npm run dev
```

---

## 🔑 Variáveis de Ambiente

```env
# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/chronosbot
# fallback para desenvolvimento: DATABASE_URL=sqlite:///./chronosbot.db

# Segurança
JWT_SECRET_KEY=troque-por-uma-chave-secreta-forte
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_data
```

> ⚠️ Nunca commite o arquivo `.env`. Ele já deve constar no `.gitignore`.

---

## 🗺️ Roadmap

- [x] Modelagem relacional (`models.py`)
- [x] Autenticação JWT + bcrypt (`auth.py`)
- [x] Pipeline de ingestão e recuperação RAG (`rag.py`)
- [x] Geração de simulados estruturados (`simulado.py`)
- [x] Rotas de autenticação (`routes_auth.py`)
- [ ] Rotas do professor (`routes_professor.py`)
- [ ] Rotas do aluno (`routes_aluno.py`)
- [ ] Composição final da aplicação (`main.py`)
- [ ] Frontend do painel do professor
- [ ] Frontend do chat do aluno
- [ ] Testes automatizados (pytest)
- [ ] Deploy em ambiente de produção

---

## 🤝 Contribuindo

Este é um projeto acadêmico em desenvolvimento ativo. Sugestões, issues e pull requests são bem-vindos.

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature X'`)
4. Push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

---

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

<div align="center">

Desenvolvido por **Karolini R. Pedrozo** · Projeto acadêmico de Chatbot Educacional com arquitetura RAG

</div>
