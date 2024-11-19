// components/routes.js

const BASE_URL = 'http://backend_pointlojista:5000'; // Nome do serviço no Docker Compose

// Função genérica para fazer requisições HTTP
const apiRequest = async (endpoint, method = 'GET', data = null) => {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);

        if (!response.ok) {
            throw new Error(`Erro na requisição para ${endpoint}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`Erro na requisição para ${endpoint}:`, error);
        throw error;
    }
};

// Funções específicas para as rotas

export const getUsers = () => apiRequest('/list_users'); // GET
export const createUser = (userData) => apiRequest('/create_user', 'POST', userData); // POST
export const updateUser = (userData) => apiRequest('/upload_user', 'PUT', userData); // PUT
export const deleteUser = (userId) => apiRequest('/delete_user', 'DELETE', { id: userId }); // DELETE
