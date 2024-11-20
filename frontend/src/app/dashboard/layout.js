"use client";
import React, { useState } from 'react';
import Sidebar from '../../components/sidebar/Sidebar'; // Importando o componente Sidebar
import { FiUsers, FiMenu } from 'react-icons/fi'; // Importando o ícone do hamburguer

const Dashboard = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleSidebarItemClick = () => {
    // Fecha o sidebar ao clicar em um item
    setIsSidebarOpen(false);
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Barra Superior com Borda Inferior */}
      <div className="bg-gray-800 text-white p-4 flex justify-between items-center border-b border-gray-600">
        <div className="flex items-center space-x-4">
          {/* Botão Hamburguer no lado esquerdo */}
          <button onClick={toggleSidebar} className="sm:hidden text-white">
            <FiMenu size={24} />
          </button>
          <div className="text-xl">Dashboard</div>
        </div>

        {/* Itens à direita da barra */}
        <div className="flex items-center">
          <span className="mr-4">Settings</span>
          <span className="bg-gray-700 rounded-full p-2">
            {/* Ícone de perfil */}
            <FiUsers size={20} />
          </span>
        </div>
      </div>

      <div className="flex flex-1">
        {/* Barra Lateral Importada */}
        <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} onItemClick={handleSidebarItemClick} /> {/* Passando a lógica do toggle */}

        {/* Conteúdo Principal */}
        <div className="flex-1 bg-gray-100 p-6">
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-gray-800 p-4 shadow-md rounded-md">
              <h2 className="text-xl font-semibold mb-2 text-white">Total Sales</h2>
              <p className="text-2xl text-white">$12,345</p>
            </div>
            <div className="bg-gray-800 p-4 shadow-md rounded-md">
              <h2 className="text-xl font-semibold mb-2 text-white">New Orders</h2>
              <p className="text-2xl text-white">350</p>
            </div>
            <div className="bg-gray-800 p-4 shadow-md rounded-md">
              <h2 className="text-xl font-bold mb-2 text-white">Customers</h2>
              <p className="text-2xl text-white">1,245</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;




