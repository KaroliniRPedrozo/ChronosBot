# ChronosBot — Frontend

Interface web do ChronosBot: chat estilo ChatGPT/Gemini para o aluno e
dashboard de gestão de conteúdo para o professor.

## Setup

```bash
npm install
cp .env.example .env
# ajuste VITE_API_URL se o backend não estiver em localhost:8000
npm run dev
```

Acesse `http://localhost:5173`.

## Identidade visual

Em vez dos clichês visuais mais comuns em interfaces geradas por IA (fundo
creme + acento terracota, ou fundo quase-preto + neon), o ChronosBot usa:

- **Cores**: azul-tinta profundo (`--bg-app`), latão envelhecido para
  História (`--accent-historia`) e verde topográfico para Geografia
  (`--accent-geografia`) — remetendo a mapas antigos e instrumentos de
  navegação (bússola, atlas).
- **Tipografia**: `Fraunces` (serifada, com peso editorial de livro
  didático) para títulos e a marca; `Inter` para o corpo do texto e chat;
  `JetBrains Mono` para códigos de convite e metadados.
- **Elemento de assinatura**: uma "linha de contorno topográfico" (como as
  curvas de nível de um mapa de relevo) usada como divisor entre seções, no
  lugar de uma linha reta genérica.
- **Tema claro/escuro**: alternável a qualquer momento, com paleta própria
  para cada modo (não é apenas inverter cores).

## Logo

Se existir um arquivo em `src/assets/logo.png`, ele é usado automaticamente
no lugar do ícone de bússola em SVG (ver `src/components/Marca.jsx`). Basta
colocar o arquivo `logo.png` nessa pasta.

## Estrutura

```
src/
  api/client.js          -> instância axios com interceptor de JWT
  context/                -> AuthContext (login/registro/logout) e ThemeContext
  components/              -> Marca, BarraLateral, BolhaMensagem, etc.
  pages/
    Login.jsx / Registrar.jsx
    ChatAluno.jsx          -> interface de chat com o tutor IA
    DashboardProfessor.jsx -> turmas, upload/liberação de materiais
  styles/tokens.css        -> design tokens (cores, tipografia, temas)
```

## Integração com o backend

Todas as chamadas usam os endpoints documentados no `README.md` do
backend (`/auth`, `/professor`, `/aluno`). O token JWT é salvo em
`localStorage` e anexado automaticamente pelo interceptor do axios.
