import { useTheme } from "../context/ThemeContext";

export default function AlternadorTema() {
  const { tema, alternarTema } = useTheme();
  const escuro = tema === "escuro";

  return (
    <button
      onClick={alternarTema}
      aria-label={escuro ? "Mudar para tema claro" : "Mudar para tema escuro"}
      title={escuro ? "Tema claro" : "Tema escuro"}
      style={{
        width: 38,
        height: 38,
        borderRadius: 10,
        border: "1px solid var(--border)",
        background: "var(--bg-panel-raised)",
        color: "var(--ink)",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 16,
      }}
    >
      {escuro ? "☾" : "☀"}
    </button>
  );
}
