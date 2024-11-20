"use client";

import React from 'react';
import Link from 'next/link';
import { FaListOl } from "react-icons/fa";
import { BiSolidDashboard } from 'react-icons/bi';
import { GiAutoRepair } from "react-icons/gi";
import { FiUsers, FiBox, FiGitBranch } from 'react-icons/fi';

const Sidebar = ({ isOpen, toggleSidebar, onItemClick }) => {
  return (
    <div className={`w-64 bg-gray-800 text-white h-screen fixed z-50 transition-transform transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} sm:relative sm:translate-x-0`}>
      <div className="mt-6">
        <ul className="space-y-4">
          {/* Item Dashboard */}
          <li>
            <Link href="/dashboard" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <BiSolidDashboard className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Dashboard</span>
            </Link>
          </li>

          {/* Item Serviços */}
          <li>
            <Link href="/inbox" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <GiAutoRepair className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Serviços</span>
            </Link>
          </li>

          {/* Item Usuários */}
          <li>
            <Link href="/users" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <FiUsers className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Usuários</span>
            </Link>
          </li>

          {/* Item Produtos */}
          <li>
            <Link href="/products" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <FiBox className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Produtos</span>
            </Link>
          </li>

          {/* Item Tarefas */}
          <li>
            <Link href="#" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <FaListOl className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Tarefas</span>
            </Link>
          </li>

          {/* Item Git Branch */}
          <li>
            <Link href="/branch" className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 hover:bg-opacity-50 group" onClick={onItemClick}>
              <FiGitBranch className="flex-shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" />
              <span className="flex-1 ml-3 whitespace-nowrap font-bold text-white">Branch</span>
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
