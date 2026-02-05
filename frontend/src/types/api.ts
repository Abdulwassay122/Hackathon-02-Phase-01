// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Task Types
export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

// Task Creation/Update Types
export interface TaskCreate {
  title: string;
  description?: string;
  completed: boolean;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

// User Types
export interface User {
  id: string;
  email: string;
  name?: string;
}

// Authentication Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface JwtPayload {
  sub: string; // user id
  email: string;
  iat: number; // issued at
  exp: number; // expiration
}