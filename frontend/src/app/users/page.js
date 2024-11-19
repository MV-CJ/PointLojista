// app/users/page.js
'use client';

import React, { useEffect, useState } from 'react';
import { Routes } from '../components/routes/routes';

const Users = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        // Requisição para listar os usuários
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

export default Users;
