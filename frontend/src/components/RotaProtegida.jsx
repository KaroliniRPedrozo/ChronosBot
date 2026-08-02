import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RotaProtegida({ papelExigido, children }) {
  const { usuario } = useAuth();

  if (!usuario) return <Navigate to="/login" replace />;
  if (papelExigido && usuario.papel !== papelExigido) {
    return <Navigate to={usuario.papel === "professor" ? "/professor" : "/aluno"} replace />;
  }
  return children;
}
