// Usando variáveis de ambiente para armazenar as URLs da API
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const authRoute = `${API_URL}/auth`;
export const userRoute = `${API_URL}/user`;
export const productRoute = `${API_URL}/product`;
// Adicione mais rotas conforme necessário
