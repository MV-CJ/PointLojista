'use client'; // Marcar este arquivo como um Client Component

import Users from '../routes/users'; // Importa o componente Users

const ListUsersPage = () => {
  const { users, error } = Users(); // Chama o componente Users e desestrutura os dados retornados

  if (error) {
    return <div>Erro: {error}</div>;
  }

  if (!users.length) {
    return <div>Carregando usuários...</div>;
  }

  return (
    <div>
      <h1>Lista de Usuários</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default ListUsersPage;
