import { ApiResponse, Task, TaskCreate, TaskUpdate } from "../types/api";

// API service utilities for JWT token handling
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem("token");
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  private getUserIdFromToken(): string | null {
    const token = localStorage.getItem("token");
    if (!token) return null;

    try {
      const tokenParts = token.split(".");
      if (tokenParts.length !== 3) return null;

      const payload = JSON.parse(atob(tokenParts[1]));
      return payload.sub; // assuming 'sub' contains the user ID
    } catch (e) {
      console.error("Error decoding token:", e);
      return null;
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      if (response.status === 401) {
        // Token might be expired, remove token and notify listeners
        // localStorage.removeItem('token');
        // Dispatch a custom event that components can listen for
        window.dispatchEvent(
          new CustomEvent("auth-error", { detail: { status: 401 } }),
        );
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`,
      );
    }
    // For DELETE requests, there might not be a response body
    if (response.status === 204 || response.url.includes("/delete")) {
      return {} as T;
    }
    return await response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "GET",
      headers: this.getAuthHeaders(),
    });

    return this.handleResponse<T>(response);
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response);
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "PUT",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response);
  }

  async patch<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response);
  }

  async delete(endpoint: string): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "DELETE",
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token might be expired, remove token and notify listeners
        // localStorage.removeItem('token');
        // Dispatch a custom event that components can listen for
        window.dispatchEvent(
          new CustomEvent("auth-error", { detail: { status: 401 } }),
        );
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`,
      );
    }

    return response;
  }

  // Task-specific methods
  async getTasks(): Promise<ApiResponse<{ tasks: Task[] }>> {
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error("User not authenticated");
    }
    return this.get<ApiResponse<{ tasks: Task[] }>>("/api/tasks/" + userId);
  }

  async createTask(task: TaskCreate): Promise<ApiResponse<Task>> {
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error("User not authenticated");
    }
    return this.post<ApiResponse<Task>>(`/api/tasks/${userId}`, task);
  }

  async updateTask(id: number, task: TaskUpdate): Promise<ApiResponse<Task>> {
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error("User not authenticated");
    }
    return this.put<ApiResponse<Task>>(`/api/tasks/${userId}/${id}`, task);
  }

  async deleteTask(id: number): Promise<ApiResponse<null>> {
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error("User not authenticated");
    }

    const response = await this.delete(`/api/tasks/${userId}/${id}`);

    return { success: true, message: "Task deleted successfully" };
  }

  async toggleTaskCompletion(
    id: number,
  ): Promise<ApiResponse<{ task: Task; message: string }>> {
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error("User not authenticated");
    }
    return this.patch<ApiResponse<{ task: Task; message: string }>>(
      `/api/tasks/${userId}/${id}/complete`,
      {},
    );
  }
}

export const apiService = new ApiService();
