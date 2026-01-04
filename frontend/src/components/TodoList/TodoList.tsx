// src/components/TodoList/TodoList.tsx
'use client';

import { useState, useEffect } from 'react';
import { api } from '../../lib/api';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function TodoList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await api.get('http://localhost:8000/api/tasks');

      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      } else {
        setError('Failed to fetch tasks');
      }
    } catch (err) {
      setError('An error occurred while fetching tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await api.post('http://localhost:8000/api/tasks', {
        title: newTask.title,
        description: newTask.description,
        completed: false
      });

      if (response.ok) {
        const createdTask = await response.json();
        setTasks([...tasks, createdTask]);
        setNewTask({ title: '', description: '' });
      } else {
        setError('Failed to add task');
      }
    } catch (err) {
      setError('An error occurred while adding task');
      console.error(err);
    }
  };

  const toggleTaskCompletion = async (taskId: number) => {
    try {
      const response = await api.patch(`http://localhost:8000/api/tasks/${taskId}/complete`, {});

      if (response.ok) {
        const updatedTask = (await response.json()).task;
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, completed: updatedTask.completed } : task
        ));
      } else {
        setError('Failed to update task');
      }
    } catch (err) {
      setError('An error occurred while updating task');
      console.error(err);
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      const response = await api.delete(`http://localhost:8000/api/tasks/${taskId}`);

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId));
      } else {
        setError('Failed to delete task');
      }
    } catch (err) {
      setError('An error occurred while deleting task');
      console.error(err);
    }
  };

  if (loading) return <div className="text-center py-4">Loading tasks...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      {error && (
        <div className="mb-4 bg-red-50 text-red-500 p-3 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleAddTask} className="mb-8 p-4 bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700">
              Title
            </label>
            <input
              type="text"
              id="title"
              value={newTask.title}
              onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              required
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <input
              type="text"
              id="description"
              value={newTask.description}
              onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        <div className="mt-4">
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add Task
          </button>
        </div>
      </form>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {tasks.map((task) => (
            <li key={task.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-indigo-600'}`}>
                    {task.title}
                  </p>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => toggleTaskCompletion(task.id)}
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.completed
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {task.completed ? 'Completed' : 'Pending'}
                    </button>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                {task.description && (
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">{task.description}</p>
                  </div>
                )}
                <div className="mt-2 flex justify-between text-xs text-gray-500">
                  <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                  <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}