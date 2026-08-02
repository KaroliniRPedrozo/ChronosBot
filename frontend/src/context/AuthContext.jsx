import { createContext, useContext, useState, useCallback } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => {
    const salvo = localStorage.getItem("chronosbot_usuario");
    return salvo ? JSON.parse(salvo) : null;
  });

  const login = useCallback(async (email, senha) => {
    const form = new URLSearchParams();
    form.set("username", email);
    form.set("password", senha);

    const { data } = await api.post("/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    localStorage.setItem("chronosbot_token", data.access_token);
    localStorage.setItem("chronosbot_usuario", JSON.stringify(data.usuario));
    setUsuario(data.usuario);
    return data.usuario;
  }, []);

  const registrar = useCallback(async ({ nome, email, senha, papel }) => {
    await api.post("/auth/registrar", { nome, email, senha, papel });
    return login(email, senha);
  }, [login]);

  const logout = useCallback(() => {
    localStorage.removeItem("chronosbot_token");
    localStorage.removeItem("chronosbot_usuario");
    setUsuario(null);
  }, []);

  return (
    <AuthContext.Provider value={{ usuario, login, registrar, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return ctx;
}
