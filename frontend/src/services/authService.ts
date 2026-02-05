import { apiService } from "./api";

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
  user: any; // Include user data as returned by backend
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // Call the backend API
      const response = await apiService.post<AuthResponse>(
        "/auth/login",
        credentials,
      );

      // Save the token upon successful login
      this.saveToken(response.access_token);

      return response;
    } catch (error: any) {
      // Re-throw the error so it can be handled by the calling component
      throw error;
    }
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      // Call the backend API
      const response = await apiService.post<AuthResponse>(
        "/auth/register",
        userData,
      );

      // Save the token upon successful registration
      this.saveToken(response.access_token);

      return response;
    } catch (error: any) {
      // Re-throw the error so it can be handled by the calling component
      throw error;
    }
  }

  async logout(): Promise<void> {
    // Clear the stored token from both localStorage and cookies
    this.removeToken();
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem("token");
    if (!token) {
      return false;
    }

    // Check if token is valid JWT and not expired
    try {
      const tokenParts = token.split(".");
      if (tokenParts.length !== 3) {
        return false; // Invalid JWT format
      }

      // Decode the payload (second part)
      const payload = JSON.parse(atob(tokenParts[1]));

      // Check if token is expired
      if (payload.exp && Date.now() >= payload.exp * 1000) {
        // Token is expired, remove it from storage
        localStorage.removeItem("token");
        return false;
      }

      return true;
    } catch (e) {
      // If there's an error parsing the token, treat it as invalid
      console.log(e);
      return false;
    }
  }

  saveToken(token: string): void {
    // Store in both localStorage (for client-side access) and cookie (for server-side access)
    localStorage.setItem("token", token);

    // Also store in cookie for server-side access via middleware
    // Set cookie to expire in 7 days
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + 7);
    document.cookie = `token=${token}; expires=${expirationDate.toUTCString()}; path=/; SameSite=Strict`;
  }

  getToken(): string | null {
    // Try to get from localStorage first, then fall back to cookie
    const localStorageToken = localStorage.getItem("token");
    if (localStorageToken) {
      return localStorageToken;
    }

    // Extract from cookies
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'token') {
        return value;
      }
    }

    return null;
  }

  removeToken(): void {
    // Remove from both localStorage and cookie
    localStorage.removeItem("token");
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }
}

export const authService = new AuthService();
