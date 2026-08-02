import Marca from "./Marca";
import AlternadorTema from "./AlternadorTema";
import LinhaContorno from "./LinhaContorno";
import { useAuth } from "../context/AuthContext";

export default function BarraLateral({ turmas, turmaSelecionada, aoSelecionarTurma, aoSair }) {
  const { usuario } = useAuth();

  return (
    <aside
      style={{
        width: 280,
        background: "var(--bg-panel)",
        borderRight: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        height: "100%",
      }}
    >
      <div style={{ padding: "20px 18px 14px" }}>
        <Marca />
      </div>
      <LinhaContorno />

      <div style={{ padding: "16px 18px 8px", fontSize: 12, letterSpacing: "0.06em", color: "var(--ink-faint)", textTransform: "uppercase" }}>
        Suas turmas
      </div>

      <nav className="scrollbar-fina" style={{ flex: 1, overflowY: "auto", padding: "0 10px" }}>
        {turmas.length === 0 && (
          <p style={{ padding: "0 8px", fontSize: 13.5, color: "var(--ink-muted)" }}>
            Nenhuma turma ainda. Peça o código de convite ao seu professor.
          </p>
        )}
        {turmas.map((turma) => {
          const ativa = turma.id === turmaSelecionada?.id;
          const corDisciplina =
            turma.disciplina === "Historia" ? "var(--accent-historia)" : "var(--accent-geografia)";
          return (
            <button
              key={turma.id}
              onClick={() => aoSelecionarTurma(turma)}
              style={{
                width: "100%",
                textAlign: "left",
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 10px",
                marginBottom: 4,
                borderRadius: 10,
                border: "none",
                cursor: "pointer",
                background: ativa ? "var(--bg-panel-raised)" : "transparent",
                color: "var(--ink)",
              }}
            >
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: corDisciplina,
                  flexShrink: 0,
                }}
              />
              <span style={{ fontSize: 14, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {turma.nome}
              </span>
            </button>
          );
        })}
      </nav>

      <LinhaContorno cor="var(--accent-historia)" />
      <div style={{ padding: "14px 18px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ overflow: "hidden" }}>
          <div style={{ fontSize: 13.5, fontWeight: 600, whiteSpace: "nowrap", textOverflow: "ellipsis", overflow: "hidden" }}>
            {usuario?.nome}
          </div>
          <button
            onClick={aoSair}
            style={{ background: "none", border: "none", color: "var(--ink-faint)", fontSize: 12, cursor: "pointer", padding: 0 }}
          >
            Sair
          </button>
        </div>
        <AlternadorTema />
      </div>
    </aside>
  );
}
