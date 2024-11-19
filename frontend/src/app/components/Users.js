import React, { useEffect, useState } from 'react';
import { Routes } from './routes/routes';  // Importando as rotas centralizadas

const FetchUsers = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        // Fazendo uma requisição para a rota listUsers
        fetch(Routes.listUsers)
            .then((response) => response.json())
            .then((data) => setUsers(data))
            .catch((error) => console.error('Error fetching users:', error));
    }, []);

    return (
        <div>
            <h1>Users List</h1>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>
                        {user.name} - {user.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default FetchUsers;
