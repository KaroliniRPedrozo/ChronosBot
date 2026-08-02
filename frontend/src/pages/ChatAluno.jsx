import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import BarraLateral from "../components/BarraLateral";
import BolhaMensagem from "../components/BolhaMensagem";
import IndicadorDigitando from "../components/IndicadorDigitando";
import LinhaContorno from "../components/LinhaContorno";

export default function ChatAluno() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [turmas, setTurmas] = useState([]);
  const [turmaSelecionada, setTurmaSelecionada] = useState(null);
  const [sessaoId, setSessaoId] = useState(null);
  const [mensagens, setMensagens] = useState([]);
  const [pergunta, setPergunta] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [codigoConvite, setCodigoConvite] = useState("");
  const [erroConvite, setErroConvite] = useState("");
  const fimDaListaRef = useRef(null);

  useEffect(() => {
    carregarTurmas();
  }, []);

  useEffect(() => {
    fimDaListaRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [mensagens, enviando]);

  async function carregarTurmas() {
    const { data } = await api.get("/aluno/turmas");
    setTurmas(data);
    if (data.length > 0 && !turmaSelecionada) {
      setTurmaSelecionada(data[0]);
    }
  }

  function selecionarTurma(turma) {
    setTurmaSelecionada(turma);
    setSessaoId(null);
    setMensagens([]);
  }

  async function entrarNaTurma(e) {
    e.preventDefault();
    setErroConvite("");
    try {
      await api.post("/aluno/turmas/entrar", { codigo_convite: codigoConvite.trim() });
      setCodigoConvite("");
      await carregarTurmas();
    } catch (err) {
      setErroConvite(err.response?.data?.detail || "Código inválido.");
    }
  }

  async function enviarPergunta(e) {
    e.preventDefault();
    if (!pergunta.trim() || !turmaSelecionada || enviando) return;

    const textoPergunta = pergunta.trim();
    setPergunta("");
    setMensagens((atual) => [...atual, { remetente: "aluno", conteudo: textoPergunta }]);
    setEnviando(true);

    try {
      const { data } = await api.post("/aluno/chat", {
        turma_id: turmaSelecionada.id,
        sessao_id: sessaoId,
        pergunta: textoPergunta,
      });
      setSessaoId(data.sessao_id);
      setMensagens((atual) => [...atual, { remetente: "assistente", conteudo: data.resposta }]);
    } catch (err) {
      setMensagens((atual) => [
        ...atual,
        {
          remetente: "assistente",
          conteudo:
            err.response?.data?.detail ||
            "Não consegui responder agora. Tente novamente em instantes.",
        },
      ]);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <BarraLateral
        turmas={turmas}
        turmaSelecionada={turmaSelecionada}
        aoSelecionarTurma={selecionarTurma}
        aoSair={() => {
          logout();
          navigate("/login");
        }}
      />

      <main style={{ flex: 1, display: "flex", flexDirection: "column", background: "var(--bg-app)" }}>
        {!turmaSelecionada ? (
          <div style={{ margin: "auto", textAlign: "center", maxWidth: 380, padding: 20 }}>
            <h2 className="fonte-display" style={{ marginBottom: 8 }}>Entre em uma turma</h2>
            <p style={{ color: "var(--ink-muted)", fontSize: 14, marginBottom: 20 }}>
              Peça ao seu professor o código de convite da turma.
            </p>
            <form onSubmit={entrarNaTurma} style={{ display: "flex", gap: 8 }}>
              <input
                value={codigoConvite}
                onChange={(e) => setCodigoConvite(e.target.value)}
                placeholder="Código de convite"
                style={{
                  flex: 1,
                  padding: "10px 12px",
                  borderRadius: 9,
                  border: "1px solid var(--border)",
                  background: "var(--bg-input)",
                  color: "var(--ink)",
                }}
              />
              <button
                type="submit"
                style={{
                  padding: "10px 16px",
                  borderRadius: 9,
                  border: "none",
                  background: "var(--accent-geografia)",
                  color: "var(--bg-app)",
                  fontWeight: 600,
                  cursor: "pointer",
                }}
              >
                Entrar
              </button>
            </form>
            {erroConvite && <p style={{ color: "var(--perigo)", fontSize: 13, marginTop: 10 }}>{erroConvite}</p>}
          </div>
        ) : (
          <>
            <header style={{ padding: "16px 24px", borderBottom: "1px solid var(--border)" }}>
              <h2 className="fonte-display" style={{ margin: 0, fontSize: 18 }}>
                {turmaSelecionada.nome}
              </h2>
              <span style={{ fontSize: 12.5, color: "var(--ink-faint)" }}>
                {turmaSelecionada.disciplina === "Historia" ? "História" : "Geografia"}
              </span>
            </header>

            <div className="scrollbar-fina" style={{ flex: 1, overflowY: "auto", padding: "20px 24px" }}>
              {mensagens.length === 0 && (
                <div style={{ textAlign: "center", marginTop: 60, color: "var(--ink-faint)" }}>
                  <p className="fonte-display" style={{ fontSize: 20, color: "var(--ink-muted)" }}>
                    O que você quer estudar hoje?
                  </p>
                  <p style={{ fontSize: 13.5 }}>Pergunte sobre qualquer material liberado nesta turma.</p>
                </div>
              )}
              {mensagens.map((m, i) => (
                <BolhaMensagem key={i} remetente={m.remetente} conteudo={m.conteudo} />
              ))}
              {enviando && <IndicadorDigitando />}
              <div ref={fimDaListaRef} />
            </div>

            <LinhaContorno />

            <form onSubmit={enviarPergunta} style={{ padding: 18, display: "flex", gap: 10 }}>
              <input
                value={pergunta}
                onChange={(e) => setPergunta(e.target.value)}
                placeholder="Pergunte ao ChronosBot…"
                style={{
                  flex: 1,
                  padding: "13px 16px",
                  borderRadius: 12,
                  border: "1px solid var(--border)",
                  background: "var(--bg-input)",
                  color: "var(--ink)",
                  fontSize: 14.5,
                }}
              />
              <button
                type="submit"
                disabled={enviando || !pergunta.trim()}
                style={{
                  padding: "0 20px",
                  borderRadius: 12,
                  border: "none",
                  background: "var(--accent-geografia)",
                  color: "var(--bg-app)",
                  fontWeight: 600,
                  cursor: "pointer",
                  opacity: enviando || !pergunta.trim() ? 0.6 : 1,
                }}
              >
                Enviar
              </button>
            </form>
          </>
        )}
      </main>
    </div>
  );
}
