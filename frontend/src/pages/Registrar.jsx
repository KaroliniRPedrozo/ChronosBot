import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../api/client";
import Marca from "../components/Marca";
import LinhaContorno from "../components/LinhaContorno";

export default function Registrar() {
  const { registrar } = useAuth();
  const navigate = useNavigate();
  const [dados, setDados] = useState({ nome: "", email: "", senha: "", papel: "aluno", codigo_turma: "" });
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  function atualizar(campo, valor) {
    setDados((d) => ({ ...d, [campo]: valor }));
  }

  async function aoSubmeter(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);

    try {
      const usuario = await registrar(dados);

      if (dados.papel === "aluno" && dados.codigo_turma.trim()) {
        try {
          await api.post(
            "/aluno/turmas/entrar",
            { codigo_convite: dados.codigo_turma.trim() },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("chronosbot_token")}`,
              },
            }
          );
        } catch (err) {
          console.warn("Não foi possível entrar na turma automaticamente:", err);
        }
      }

      navigate(usuario.papel === "professor" ? "/professor" : "/aluno");
    } catch (err) {
      setErro(err.response?.data?.detail || "Não foi possível criar sua conta.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div style={estilos.pagina}>
      <div style={estilos.cartao}>
        <Marca tamanho={34} />
        <p style={{ color: "var(--ink-muted)", fontSize: 14, marginTop: 10, marginBottom: 20 }}>
          Crie sua conta para começar.
        </p>
        <LinhaContorno cor="var(--accent-historia)" />

        <div style={{ display: "flex", gap: 8, margin: "20px 0" }}>
          {[
            { valor: "aluno", rotulo: "Sou aluno" },
            { valor: "professor", rotulo: "Sou professor" },
          ].map((op) => (
            <button
              type="button"
              key={op.valor}
              onClick={() => atualizar("papel", op.valor)}
              style={{
                flex: 1,
                padding: "10px 0",
                borderRadius: 9,
                border: `1px solid ${dados.papel === op.valor ? "var(--accent-geografia)" : "var(--border)"}`,
                background: dados.papel === op.valor ? "var(--bg-panel-raised)" : "transparent",
                color: "var(--ink)",
                cursor: "pointer",
                fontSize: 13.5,
                fontWeight: dados.papel === op.valor ? 600 : 400,
              }}
            >
              {op.rotulo}
            </button>
          ))}
        </div>

        <form onSubmit={aoSubmeter} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <label style={estilos.rotulo}>
            Nome
            <input
              required
              value={dados.nome}
              onChange={(e) => atualizar("nome", e.target.value)}
              style={estilos.input}
              placeholder="Seu nome completo"
            />
          </label>
          <label style={estilos.rotulo}>
            E-mail
            <input
              type="email"
              required
              value={dados.email}
              onChange={(e) => atualizar("email", e.target.value)}
              style={estilos.input}
              placeholder="seu@email.com"
            />
          </label>
          <label style={estilos.rotulo}>
            Senha
            <input
              type="password"
              required
              minLength={8}
              value={dados.senha}
              onChange={(e) => atualizar("senha", e.target.value)}
              style={estilos.input}
              placeholder="Mínimo 8 caracteres"
            />
          </label>
          {dados.papel === "aluno" && (
            <label style={estilos.rotulo}>
              Código da turma
              <input
                value={dados.codigo_turma}
                onChange={(e) => atualizar("codigo_turma", e.target.value)}
                style={estilos.input}
                placeholder="Digite o código de convite"
              />
            </label>
          )}

          {erro && <p style={{ color: "var(--perigo)", fontSize: 13.5, margin: 0 }}>{erro}</p>}

          <button type="submit" disabled={carregando} style={estilos.botao}>
            {carregando ? "Criando conta…" : "Criar conta"}
          </button>
        </form>

        <p style={{ fontSize: 13.5, color: "var(--ink-muted)", marginTop: 20, textAlign: "center" }}>
          Já tem conta? <Link to="/login" style={{ color: "var(--accent-geografia)" }}>Entrar</Link>
        </p>
      </div>
    </div>
  );
}

const estilos = {
  pagina: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 20 },
  cartao: {
    width: "100%",
    maxWidth: 400,
    background: "var(--bg-panel)",
    border: "1px solid var(--border)",
    borderRadius: 16,
    padding: 32,
    boxShadow: "var(--sombra)",
  },
  rotulo: { display: "flex", flexDirection: "column", gap: 6, fontSize: 13, color: "var(--ink-muted)" },
  input: {
    padding: "10px 12px",
    borderRadius: 9,
    border: "1px solid var(--border)",
    background: "var(--bg-input)",
    color: "var(--ink)",
    fontSize: 14.5,
  },
  botao: {
    marginTop: 6,
    padding: "11px 16px",
    borderRadius: 9,
    border: "none",
    background: "var(--accent-historia)",
    color: "var(--bg-app)",
    fontWeight: 600,
    fontSize: 14.5,
    cursor: "pointer",
  },
};
