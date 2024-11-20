import { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchUsers() {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/list_users`);
        if (!response.ok) {
          throw new Error('Erro ao carregar usuários');
        }
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchUsers();
  }, []);

  if (error) {
    return { error }; // Retorna o erro
  }

  return { users }; // Retorna os usuários
};

export default Users;
