// login/page.tsx (ou page.jsx se preferir a extensão .jsx)
'use client';

import { useState } from "react";
import { useRouter } from 'next/navigation';
import { login, fetchUserProfile } from '../services/auth'; // Ajuste o caminho conforme a estrutura do seu projeto

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [responseMessage, setResponseMessage] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await login(email, password);
      setResponseMessage("Login bem-sucedido!");
      
      if (response?.token) {
        const profileData = await fetchUserProfile(response.token);
        console.log("Dados do perfil:", profileData);
      }

      router.push('/dashboard');
    } catch (error) {
      setResponseMessage("Erro ao fazer login. Verifique suas credenciais.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", textAlign: "center" }}>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: "10px" }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
              backgroundColor: "#f0f0f0",
            }}
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
              backgroundColor: "#f0f0f0",
            }}
          />
        </div>
        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "blue",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          Login
        </button>
      </form>

      {/* Exibição de mensagem de resposta */}
      {responseMessage && (
        <div
          style={{
            marginTop: "20px",
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "5px",
            backgroundColor: "#f9f9f9",
          }}
        >
          {responseMessage}
        </div>
      )}
    </div>
  );
}