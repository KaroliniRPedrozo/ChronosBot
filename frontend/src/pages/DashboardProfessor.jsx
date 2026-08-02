import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import Marca from "../components/Marca";
import AlternadorTema from "../components/AlternadorTema";
import LinhaContorno from "../components/LinhaContorno";

const RÓTULOS_STATUS = {
  pendente: "Aguardando processamento",
  processando: "Processando…",
  concluido: "Pronto",
  erro: "Erro no processamento",
};

export default function DashboardProfessor() {
  const { usuario, logout } = useAuth();
  const navigate = useNavigate();

  const [turmas, setTurmas] = useState([]);
  const [materiais, setMateriais] = useState([]);
  const [abaAtiva, setAbaAtiva] = useState("turmas");

  const [novaTurma, setNovaTurma] = useState({ nome: "", disciplina: "Historia" });
  const [novoMaterial, setNovoMaterial] = useState({ titulo: "", disciplina: "Historia", arquivo: null });
  const [liberacao, setLiberacao] = useState({ materialId: "", turmaIds: [], dataLiberacao: "" });
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    carregarTudo();
  }, []);

  async function carregarTudo() {
    const [respTurmas, respMateriais] = await Promise.all([
      api.get("/professor/turmas"),
      api.get("/professor/materiais"),
    ]);
    setTurmas(respTurmas.data);
    setMateriais(respMateriais.data);
  }

  async function criarTurma(e) {
    e.preventDefault();
    await api.post("/professor/turmas", novaTurma);
    setNovaTurma({ nome: "", disciplina: "Historia" });
    await carregarTudo();
  }

  async function enviarMaterial(e) {
    e.preventDefault();
    if (!novoMaterial.arquivo) return;

    const form = new FormData();
    form.append("titulo", novoMaterial.titulo);
    form.append("disciplina", novoMaterial.disciplina);
    form.append("arquivo", novoMaterial.arquivo);

    await api.post("/professor/materiais", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setNovoMaterial({ titulo: "", disciplina: "Historia", arquivo: null });
    setMensagem("Material enviado. O processamento roda em segundo plano.");
    await carregarTudo();
  }

  async function liberarMaterial(e) {
    e.preventDefault();
    if (!liberacao.materialId || liberacao.turmaIds.length === 0 || !liberacao.dataLiberacao) return;

    await api.post(`/professor/materiais/${liberacao.materialId}/liberar`, {
      turma_ids: liberacao.turmaIds,
      data_liberacao: new Date(liberacao.dataLiberacao).toISOString(),
    });
    setMensagem("Material liberado com sucesso.");
    setLiberacao({ materialId: "", turmaIds: [], dataLiberacao: "" });
  }

  function alternarTurmaNaLiberacao(id) {
    setLiberacao((atual) => ({
      ...atual,
      turmaIds: atual.turmaIds.includes(id)
        ? atual.turmaIds.filter((t) => t !== id)
        : [...atual.turmaIds, id],
    }));
  }

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg-app)" }}>
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "16px 28px",
          borderBottom: "1px solid var(--border)",
        }}
      >
        <Marca />
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span style={{ fontSize: 13.5, color: "var(--ink-muted)" }}>{usuario?.nome}</span>
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
            style={{ background: "none", border: "1px solid var(--border)", borderRadius: 8, padding: "7px 12px", color: "var(--ink)", cursor: "pointer", fontSize: 13 }}
          >
            Sair
          </button>
          <AlternadorTema />
        </div>
      </header>
      <LinhaContorno />

      <nav style={{ display: "flex", gap: 4, padding: "18px 28px 0" }}>
        {[
          { id: "turmas", rotulo: "Turmas" },
          { id: "materiais", rotulo: "Materiais" },
          { id: "liberar", rotulo: "Liberar conteúdo" },
        ].map((aba) => (
          <button
            key={aba.id}
            onClick={() => setAbaAtiva(aba.id)}
            style={{
              padding: "9px 16px",
              borderRadius: "10px 10px 0 0",
              border: "1px solid var(--border)",
              borderBottom: abaAtiva === aba.id ? "2px solid var(--bg-app)" : "1px solid var(--border)",
              background: abaAtiva === aba.id ? "var(--bg-panel)" : "transparent",
              color: "var(--ink)",
              cursor: "pointer",
              fontSize: 14,
              fontWeight: abaAtiva === aba.id ? 600 : 400,
            }}
          >
            {aba.rotulo}
          </button>
        ))}
      </nav>

      <main style={{ padding: 28, maxWidth: 760 }}>
        {mensagem && (
          <p style={{ background: "var(--bg-panel-raised)", border: "1px solid var(--border)", borderRadius: 10, padding: "10px 14px", fontSize: 13.5, marginBottom: 20 }}>
            {mensagem}
          </p>
        )}

        {abaAtiva === "turmas" && (
          <section>
            <h3 className="fonte-display">Criar nova turma</h3>
            <form onSubmit={criarTurma} style={{ display: "flex", gap: 10, marginBottom: 28, flexWrap: "wrap" }}>
              <input
                required
                placeholder="Nome da turma (ex: 3º Ano B — Manhã)"
                value={novaTurma.nome}
                onChange={(e) => setNovaTurma((d) => ({ ...d, nome: e.target.value }))}
                style={{ flex: 1, minWidth: 220, ...estiloInput }}
              />
              <select
                value={novaTurma.disciplina}
                onChange={(e) => setNovaTurma((d) => ({ ...d, disciplina: e.target.value }))}
                style={estiloInput}
              >
                <option value="Historia">História</option>
                <option value="Geografia">Geografia</option>
              </select>
              <button type="submit" style={estiloBotao}>Criar</button>
            </form>

            <h3 className="fonte-display">Suas turmas</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {turmas.map((t) => (
                <div key={t.id} style={estiloCartao}>
                  <div>
                    <strong>{t.nome}</strong>
                    <span style={{ marginLeft: 8, fontSize: 12.5, color: "var(--ink-faint)" }}>
                      {t.disciplina === "Historia" ? "História" : "Geografia"}
                    </span>
                  </div>
                  <span className="fonte-mono" style={{ fontSize: 12.5, color: "var(--accent-geografia)" }}>
                    código: {t.codigo_convite}
                  </span>
                </div>
              ))}
              {turmas.length === 0 && <p style={{ color: "var(--ink-muted)", fontSize: 13.5 }}>Nenhuma turma criada ainda.</p>}
            </div>
          </section>
        )}

        {abaAtiva === "materiais" && (
          <section>
            <h3 className="fonte-display">Enviar material</h3>
            <form onSubmit={enviarMaterial} style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 28 }}>
              <input
                required
                placeholder="Título do material"
                value={novoMaterial.titulo}
                onChange={(e) => setNovoMaterial((d) => ({ ...d, titulo: e.target.value }))}
                style={estiloInput}
              />
              <select
                value={novoMaterial.disciplina}
                onChange={(e) => setNovoMaterial((d) => ({ ...d, disciplina: e.target.value }))}
                style={estiloInput}
              >
                <option value="Historia">História</option>
                <option value="Geografia">Geografia</option>
              </select>
              <input
                required
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setNovoMaterial((d) => ({ ...d, arquivo: e.target.files[0] }))}
                style={estiloInput}
              />
              <button type="submit" style={{ ...estiloBotao, alignSelf: "flex-start" }}>Enviar material</button>
            </form>

            <h3 className="fonte-display">Materiais enviados</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {materiais.map((m) => (
                <div key={m.id} style={estiloCartao}>
                  <div>
                    <strong>{m.titulo}</strong>
                    <span style={{ marginLeft: 8, fontSize: 12.5, color: "var(--ink-faint)" }}>
                      {m.disciplina === "Historia" ? "História" : "Geografia"}
                    </span>
                  </div>
                  <span style={{ fontSize: 12.5, color: m.status_processamento === "erro" ? "var(--perigo)" : "var(--ink-muted)" }}>
                    {RÓTULOS_STATUS[m.status_processamento]}
                  </span>
                </div>
              ))}
              {materiais.length === 0 && <p style={{ color: "var(--ink-muted)", fontSize: 13.5 }}>Nenhum material enviado ainda.</p>}
            </div>
          </section>
        )}

        {abaAtiva === "liberar" && (
          <section>
            <h3 className="fonte-display">Liberar material para turmas</h3>
            <form onSubmit={liberarMaterial} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              <label style={estiloRotulo}>
                Material
                <select
                  required
                  value={liberacao.materialId}
                  onChange={(e) => setLiberacao((d) => ({ ...d, materialId: e.target.value }))}
                  style={estiloInput}
                >
                  <option value="">Selecione um material pronto</option>
                  {materiais
                    .filter((m) => m.status_processamento === "concluido")
                    .map((m) => (
                      <option key={m.id} value={m.id}>{m.titulo}</option>
                    ))}
                </select>
              </label>

              <div>
                <span style={{ ...estiloRotulo, marginBottom: 8, display: "block" }}>Turmas</span>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                  {turmas.map((t) => (
                    <button
                      type="button"
                      key={t.id}
                      onClick={() => alternarTurmaNaLiberacao(t.id)}
                      style={{
                        padding: "7px 12px",
                        borderRadius: 999,
                        border: `1px solid ${liberacao.turmaIds.includes(t.id) ? "var(--accent-geografia)" : "var(--border)"}`,
                        background: liberacao.turmaIds.includes(t.id) ? "var(--bg-panel-raised)" : "transparent",
                        color: "var(--ink)",
                        fontSize: 13,
                        cursor: "pointer",
                      }}
                    >
                      {t.nome}
                    </button>
                  ))}
                </div>
              </div>

              <label style={estiloRotulo}>
                Liberar a partir de
                <input
                  required
                  type="datetime-local"
                  value={liberacao.dataLiberacao}
                  onChange={(e) => setLiberacao((d) => ({ ...d, dataLiberacao: e.target.value }))}
                  style={estiloInput}
                />
              </label>

              <button type="submit" style={{ ...estiloBotao, alignSelf: "flex-start" }}>Liberar</button>
            </form>
          </section>
        )}
      </main>
    </div>
  );
}

const estiloInput = {
  padding: "10px 12px",
  borderRadius: 9,
  border: "1px solid var(--border)",
  background: "var(--bg-input)",
  color: "var(--ink)",
  fontSize: 14,
};

const estiloBotao = {
  padding: "10px 18px",
  borderRadius: 9,
  border: "none",
  background: "var(--accent-historia)",
  color: "var(--bg-app)",
  fontWeight: 600,
  fontSize: 14,
  cursor: "pointer",
};

const estiloCartao = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  padding: "12px 16px",
  borderRadius: 10,
  border: "1px solid var(--border)",
  background: "var(--bg-panel)",
  fontSize: 14,
};

const estiloRotulo = { display: "flex", flexDirection: "column", gap: 6, fontSize: 13, color: "var(--ink-muted)" };
