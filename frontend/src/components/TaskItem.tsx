'use client';

import { useState } from 'react';
import { Task } from '../types/api';
import { apiService } from '../services/api';
import { ApiResponse, TaskUpdate } from '../types/api';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export default function TaskItem({ task, onTaskUpdated, onTaskDeleted }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      const response = await apiService.toggleTaskCompletion(task.id);
      if (response.success) {
        onTaskUpdated();
      }
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const taskUpdate: TaskUpdate = { title, description };
      const response: ApiResponse<Task> = await apiService.updateTask(task.id, taskUpdate);
      if (response.success) {
        onTaskUpdated();
        setIsEditing(false);
      }
    } catch (err) {
      console.error('Failed to update task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setLoading(true);
      try {
        const response = await apiService.deleteTask(task.id);
        if (response.success) {
          onTaskDeleted();
        }
      } catch (err) {
        console.error('Failed to delete task:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  if (isEditing) {
    return (
      <div className="bg-blue-50 p-6 rounded-xl shadow-md border border-blue-200">
        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label htmlFor={`title-${task.id}`} className="block text-sm font-medium text-gray-700 mb-2">
              Title *
            </label>
            <input
              id={`title-${task.id}`}
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Enter task title..."
              required
            />
          </div>
          <div>
            <label htmlFor={`description-${task.id}`} className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id={`description-${task.id}`}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              rows={4}
              placeholder="Enter task description..."
            />
          </div>
          <div className="flex space-x-3 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-2.5 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              disabled={loading}
              className="flex-1 bg-gray-200 text-gray-800 py-2.5 px-4 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  }

  return (
    <div
      className={`bg-white p-6 rounded-xl shadow-md border transition-all duration-200 hover:shadow-lg ${
        task.completed
          ? 'bg-green-50 border-green-200'
          : 'bg-white border-gray-200'
      }`}
      role="article"
      aria-labelledby={`task-title-${task.id}`}
    >
      <div className="flex justify-between items-start mb-3">
        <h3
          id={`task-title-${task.id}`}
          className={`text-lg font-semibold ${
            task.completed
              ? 'text-gray-500 line-through'
              : 'text-gray-800'
          }`}
        >
          {task.title}
        </h3>
        <span
          className={`px-2 py-1 rounded-full text-xs font-medium ${
            task.completed
              ? 'bg-green-100 text-green-800'
              : 'bg-yellow-100 text-yellow-800'
          }`}
          aria-label={task.completed ? 'Task completed' : 'Task pending'}
        >
          {task.completed ? 'Completed' : 'Pending'}
        </span>
      </div>

      {task.description && (
        <p className="text-gray-600 mb-4 text-sm" id={`task-desc-${task.id}`}>
          {task.description}
        </p>
      )}

      <div className="flex justify-between items-center text-xs text-gray-500 mb-4">
        <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
        <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
      </div>

      <div className="flex space-x-2" role="group" aria-label="Task actions">
        <button
          onClick={handleToggleComplete}
          disabled={loading}
          className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
            task.completed
              ? 'bg-green-100 text-green-800 hover:bg-green-200'
              : 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
          }`}
          aria-label={task.completed ? `Mark task "${task.title}" as incomplete` : `Mark task "${task.title}" as complete`}
        >
          {loading ? 'Saving...' : task.completed ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button
          onClick={() => setIsEditing(true)}
          disabled={loading}
          className="px-3 py-1.5 bg-blue-100 text-blue-800 rounded-md text-sm font-medium hover:bg-blue-200 transition-colors"
          aria-label={`Edit task "${task.title}"`}
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          disabled={loading}
          className="px-3 py-1.5 bg-red-100 text-red-800 rounded-md text-sm font-medium hover:bg-red-200 transition-colors"
          aria-label={`Delete task "${task.title}"`}
        >
          {loading ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  );
}