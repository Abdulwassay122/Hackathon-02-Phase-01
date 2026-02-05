'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '../../services/authService';
import TodoList from '../../components/TodoList/TodoList';
import ProtectedRoute from '../../components/ProtectedRoute';

export default function Dashboard() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4 max-w-6xl">
          <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Todo Dashboard</h1>
          <TodoList />
        </div>
      </div>
    </ProtectedRoute>
  );
}