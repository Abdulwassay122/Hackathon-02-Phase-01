'use client';

import TodoList from '../../components/TodoList/TodoList';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Todo Dashboard</h1>
        <TodoList />
      </div>
    </div>
  );
}