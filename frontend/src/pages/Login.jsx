import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Marca from "../components/Marca";
import LinhaContorno from "../components/LinhaContorno";
import AlternadorTema from "../components/AlternadorTema";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function aoSubmeter(e) {
    e.preventDefault();
    setErro("");
    setCarregando(true);
    try {
      const usuario = await login(email, senha);
      navigate(usuario.papel === "professor" ? "/professor" : "/aluno");
    } catch (err) {
      setErro(
        err.response?.data?.detail || "Não foi possível entrar. Verifique seu e-mail e senha."
      );
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div style={estilos.pagina}>
      <div style={{ position: "absolute", top: 20, right: 20 }}>
        <AlternadorTema />
      </div>
      <div style={estilos.cartao}>
        <Marca tamanho={48} />
        <p style={{ color: "var(--ink-muted)", fontSize: 14, marginTop: 10, marginBottom: 24 }}>
          Tutor de História e Geografia com IA.
        </p>
        <LinhaContorno />

        <form onSubmit={aoSubmeter} style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 14 }}>
          <label style={estilos.rotulo}>
            E-mail
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={estilos.input}
              placeholder="seu@email.com"
            />
          </label>
          <label style={estilos.rotulo}>
            Senha
            <input
              type="password"
              required
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              style={estilos.input}
              placeholder="••••••••"
            />
          </label>

          {erro && <p style={{ color: "var(--perigo)", fontSize: 13.5, margin: 0 }}>{erro}</p>}

          <button type="submit" disabled={carregando} style={estilos.botao}>
            {carregando ? "Entrando…" : "Entrar"}
          </button>
        </form>

        <p style={{ fontSize: 13.5, color: "var(--ink-muted)", marginTop: 20, textAlign: "center" }}>
          Ainda não tem conta? <Link to="/registrar" style={{ color: "var(--accent-geografia)" }}>Cadastre-se</Link>
        </p>
      </div>
    </div>
  );
}

const estilos = {
  pagina: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    padding: 20,
  },
  cartao: {
    width: "100%",
    maxWidth: 380,
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
    background: "var(--accent-geografia)",
    color: "var(--bg-app)",
    fontWeight: 600,
    fontSize: 14.5,
    cursor: "pointer",
  },
};
