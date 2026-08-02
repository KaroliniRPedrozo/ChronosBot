export default function BolhaMensagem({ remetente, conteudo }) {
  const doAluno = remetente === "aluno";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: doAluno ? "flex-end" : "flex-start",
        padding: "4px 0",
      }}
    >
      <div
        style={{
          maxWidth: "72%",
          padding: "12px 16px",
          borderRadius: doAluno ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
          background: doAluno ? "var(--accent-geografia)" : "var(--bg-panel-raised)",
          color: doAluno ? "var(--bg-app)" : "var(--ink)",
          border: doAluno ? "none" : "1px solid var(--border)",
          fontSize: 14.5,
          lineHeight: 1.55,
          whiteSpace: "pre-wrap",
        }}
      >
        {conteudo}
      </div>
    </div>
  );
}
