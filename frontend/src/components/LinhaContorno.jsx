/*
  Elemento de assinatura visual do ChronosBot: uma linha de contorno
  topográfico (como as curvas de nível de um mapa de relevo), usada como
  divisor entre seções em vez de uma <hr> genérica.
*/
export default function LinhaContorno({ cor = "var(--accent-geografia)" }) {
  return (
    <div className="linha-contorno" aria-hidden="true">
      <svg viewBox="0 0 400 10" preserveAspectRatio="none">
        <path
          d="M0,5 Q20,0 40,5 T80,5 T120,5 T160,5 T200,5 T240,5 T280,5 T320,5 T360,5 T400,5"
          fill="none"
          stroke={cor}
          strokeWidth="1"
        />
      </svg>
    </div>
  );
}
