export default function IndicadorDigitando() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 0" }}>
      <span className="fonte-mono" style={{ fontSize: 12, color: "var(--ink-faint)" }}>
        ChronosBot está consultando os materiais
      </span>
      <span className="pontos-digitando" aria-hidden="true">
        <style>{`
          .pontos-digitando::after {
            content: '';
            display: inline-block;
            width: 1.2em;
            text-align: left;
            animation: pontos 1.2s steps(4, end) infinite;
          }
          @keyframes pontos {
            0% { content: ''; }
            25% { content: '.'; }
            50% { content: '..'; }
            75% { content: '...'; }
          }
        `}</style>
      </span>
    </div>
  );
}
