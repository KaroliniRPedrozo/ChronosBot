import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import RotaProtegida from "./components/RotaProtegida";
import Login from "./pages/Login";
import Registrar from "./pages/Registrar";
import ChatAluno from "./pages/ChatAluno";
import DashboardProfessor from "./pages/DashboardProfessor";

function RotaInicial() {
  const { usuario } = useAuth();
  if (!usuario) return <Navigate to="/login" replace />;
  return <Navigate to={usuario.papel === "professor" ? "/professor" : "/aluno"} replace />;
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<RotaInicial />} />
            <Route path="/login" element={<Login />} />
            <Route path="/registrar" element={<Registrar />} />
            <Route
              path="/aluno"
              element={
                <RotaProtegida papelExigido="aluno">
                  <ChatAluno />
                </RotaProtegida>
              }
            />
            <Route
              path="/professor"
              element={
                <RotaProtegida papelExigido="professor">
                  <DashboardProfessor />
                </RotaProtegida>
              }
            />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
