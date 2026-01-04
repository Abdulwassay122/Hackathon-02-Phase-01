'use client';

import { useState, useEffect } from 'react';
import { TaskResponse } from '../../../backend/src/models/task';
import { apiService } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import ErrorDisplay from './ErrorDisplay';
import TaskItem from './TaskItem';

interface TaskListProps {
  userId: number;
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<TaskResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    fetchTasks();
  }, [userId, refreshTrigger]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.get<TaskResponse[]>('/tasks');
      setTasks(data);
    } catch (err) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleTaskDeleted = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  if (loading) return <LoadingSpinner text="Loading tasks..." />;
  if (error) return <ErrorDisplay message={error} onRetry={fetchTasks} />;

  if (tasks.length === 0) {
    return (
      <div className="bg-white p-8 rounded-xl shadow text-center border border-gray-200">
        <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">No tasks yet</h2>
        <p className="text-gray-600 mb-6">Get started by creating your first task</p>
        <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 inline-block">
          <p className="text-blue-800 text-sm">
            <span className="font-medium">Tip:</span> Use the form on the right to create a new task
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
      <div className="space-y-4">
        {tasks.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onTaskUpdated={handleTaskUpdated}
            onTaskDeleted={handleTaskDeleted}
          />
        ))}
      </div>
    </div>
  );
}