import React, { useState } from 'react';
import { Routes } from './routes/routes';  // Importando as rotas centralizadas

const CreateUser = () => {
    const [userData, setUserData] = useState({ name: '', email: '', password: '' });

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(Routes.createUser, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });
            const result = await response.json();
            console.log(result);
            // Tratamento após a criação do usuário
        } catch (error) {
            console.error('Error creating user:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Name"
                value={userData.name}
                onChange={(e) => setUserData({ ...userData, name: e.target.value })}
            />
            <input
                type="email"
                placeholder="Email"
                value={userData.email}
                onChange={(e) => setUserData({ ...userData, email: e.target.value })}
            />
            <input
                type="password"
                placeholder="Password"
                value={userData.password}
                onChange={(e) => setUserData({ ...userData, password: e.target.value })}
            />
            <button type="submit">Create User</button>
        </form>
    );
};

export default CreateUser;
