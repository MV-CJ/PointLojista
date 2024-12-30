// services/auth.js

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn, useSession } from 'next-auth/react';

// Hook personalizado para autenticação
export const useAuth = () => {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [, forceUpdate] = useState({}); // Usar objeto vazio para garantir que mudanças são detectadas

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login'); // Redireciona para a página de login caso não esteja autenticado
    }
    console.log('Status de sessão:', status);
    console.log('Sessão:', session);  // Isso mostrará toda a estrutura da sessão
    // Força um re-render ao detectar mudanças no status ou na sessão
    forceUpdate({});
  }, [status, session, router]);

  // Retorno ajustado para verificar se session e user estão definidos
  return { 
    status, 
    token: status === 'authenticated' && session && session.user ? session.user.accessToken : undefined
  };
};

// Função para realizar login
export const login = async (email, password) => {
  try {
    const response = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });

    if (response?.error) {
      throw new Error(response.error);
    }
    return response;
  } catch (error) {
    console.error("Erro durante o login:", error);
    throw error;
  }
};

// Função para buscar o perfil do usuário
export const fetchUserProfile = async (token) => {
  try {
    const response = await fetch("http://localhost:5999/api/user/profile", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, // Envia o token JWT
      },
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      console.error('Erro na resposta:', await response.text());
      throw new Error("Erro ao buscar perfil do usuário.");
    }

    const profileData = await response.json();
    console.log('Perfil do usuário recebido:', profileData);
    return profileData; // Retorna os dados do usuário
  } catch (error) {
    console.error("Erro ao buscar perfil do usuário:", error);
    throw error;
  }
};

// Hook para gerenciar o perfil do usuário
export const useUserProfile = () => {
  const { status, token } = useAuth();
  const [userProfile, setUserProfile] = useState(null);
  const [profileError, setProfileError] = useState(null);

  useEffect(() => {
    const loadProfile = async () => {
      if (status === 'authenticated' && token) {
        try {
          const profile = await fetchUserProfile(token);
          console.log('Perfil carregado:', profile);
          setUserProfile(profile);
        } catch (error) {
          console.error('Erro ao carregar perfil do usuário:', error.message);
          setProfileError('Erro ao carregar perfil do usuário.');
        }
      } else {
        console.log('Usuário não autenticado ou sem token:', { status, token });
      }
    };

    loadProfile();
  }, [status, token]);

  return { userProfile, profileError, isLoading: status === 'loading' };
};