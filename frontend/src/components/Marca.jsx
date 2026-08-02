/*
  Marca do ChronosBot: um losango de bússola simplificado, no lugar de um
  ícone de robô genérico — reforça a identidade de "navegação pelo tempo e
  pelo espaço" (História + Geografia). Se `logo.png` estiver disponível em
  /src/assets/logo.png, ele é usado no lugar deste SVG.
*/
import { useState } from "react";
import logo from "../assets/logo.png";

export default function Marca({ tamanho = 28, comTexto = true }) {
  const [imagemFalhou, setImagemFalhou] = useState(false);

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
      {!imagemFalhou ? (
        <img
          src={logo}
          alt="ChronosBot"
          width={tamanho}
          height={tamanho}
          style={{ borderRadius: 6, objectFit: "cover" }}
          onError={() => setImagemFalhou(true)}
        />
      ) : (
        <svg width={tamanho} height={tamanho} viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="14.5" stroke="var(--accent-historia)" strokeWidth="1.5" />
          <path d="M16 6L19 16L16 26L13 16Z" fill="var(--accent-geografia)" />
          <path d="M6 16L16 13L26 16L16 19Z" fill="var(--accent-historia)" opacity="0.85" />
          <circle cx="16" cy="16" r="2" fill="var(--bg-app)" stroke="var(--ink)" strokeWidth="0.75" />
        </svg>
      )}
      {comTexto && (
        <span className="fonte-display" style={{ fontSize: 18, fontWeight: 600 }}>
          Chronos<span style={{ color: "var(--accent-geografia)" }}>Bot</span>
        </span>
      )}
    </div>
  );
}
