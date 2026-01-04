import { TaskCreate, TaskUpdate, TaskResponse } from '../../../backend/src/models/task';
import { apiService } from './api';

export interface TaskService {
  getTasks: (userId: number) => Promise<TaskResponse[]>;
  createTask: (userId: number, task: TaskCreate) => Promise<TaskResponse>;
  getTask: (userId: number, taskId: number) => Promise<TaskResponse>;
  updateTask: (userId: number, taskId: number, task: TaskUpdate) => Promise<TaskResponse>;
  deleteTask: (userId: number, taskId: number) => Promise<void>;
  toggleTaskCompletion: (userId: number, taskId: number) => Promise<TaskResponse>;
}

class TaskServiceImpl implements TaskService {
  async getTasks(userId: number): Promise<TaskResponse[]> {
    return await apiService.get(`/users/${userId}/tasks`);
  }

  async createTask(userId: number, task: TaskCreate): Promise<TaskResponse> {
    return await apiService.post(`/users/${userId}/tasks`, task);
  }

  async getTask(userId: number, taskId: number): Promise<TaskResponse> {
    return await apiService.get(`/users/${userId}/tasks/${taskId}`);
  }

  async updateTask(userId: number, taskId: number, task: TaskUpdate): Promise<TaskResponse> {
    return await apiService.put(`/users/${userId}/tasks/${taskId}`, task);
  }

  async deleteTask(userId: number, taskId: number): Promise<void> {
    await apiService.delete(`/users/${userId}/tasks/${taskId}`);
  }

  async toggleTaskCompletion(userId: number, taskId: number): Promise<TaskResponse> {
    const result = await apiService.patch(`/users/${userId}/tasks/${taskId}/complete`);
    return result.task;
  }
}

export const taskService = new TaskServiceImpl();