import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
    providers: [
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" },
            },
            async authorize(credentials) {
                const res = await fetch("http://localhost:5999/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: credentials?.email,
                        password: credentials?.password,
                    }),
                });

                const data = await res.json();

                if (res.ok && data.access_token) {
                    return { token: data.access_token }; // Retorna o token como uma propriedade chamada 'token'
                } else {
                    throw new Error(data.msg || "Login failed");
                }
            },
        }),
    ],
    pages: {
        signIn: "/login",
    },
    session: {
        strategy: "jwt",
    },
    callbacks: {
        async jwt({ token, user }) {
            if (user?.token) {
                token.accessToken = user.token; // Corrigido para usar 'token' em vez de 'accessToken'
            }
            return token;
        },
        async session({ session, token }) {
            if (token?.accessToken) {
                session.user.accessToken = token.accessToken; // Adicionado 'user' para seguir as convenções de NextAuth
            }
            return session;
        },
    },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };