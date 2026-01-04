import { apiService } from './api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // In a real implementation, we would call the backend API
    // const response = await apiService.post<AuthResponse>('/auth/login', credentials);
    // For now, return mock data
    return {
      access_token: 'mock-jwt-token',
      token_type: 'bearer'
    };
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    // In a real implementation, we would call the backend API
    // const response = await apiService.post<AuthResponse>('/auth/register', userData);
    // For now, return mock data
    return {
      access_token: 'mock-jwt-token',
      token_type: 'bearer'
    };
  }

  async logout(): Promise<void> {
    // Clear the stored token
    localStorage.removeItem('access_token');
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    // In a real implementation, we would verify the token
    return !!token;
  }

  saveToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
}

export const authService = new AuthService();