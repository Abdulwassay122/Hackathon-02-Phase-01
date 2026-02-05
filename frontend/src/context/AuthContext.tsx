'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authService } from '../services/authService';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any; // Replace with proper User type
  token: string | null;
  loading: boolean;
  error: string | null;
  login: (credentials: { username: string; password: string }) => Promise<void>;
  register: (userData: { username: string; email: string; password: string }) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<any>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkAuthStatus();

    // Listen for auth-error events to handle token invalidation
    const handleAuthError = () => {
      setIsAuthenticated(false);
      setToken(null);
      setUser(null);
    };

    window.addEventListener('auth-error', handleAuthError);

    return () => {
      window.removeEventListener('auth-error', handleAuthError);
    };
  }, []);

  const checkAuthStatus = async () => {
    setLoading(true);
    try {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);

      if (authenticated) {
        const currentToken = authService.getToken();
        setToken(currentToken);
        // In a real app, you'd fetch user details here
        // setUser(fetchedUserDetails);
      } else {
        setToken(null);
        setUser(null);
      }
    } catch (err) {
      console.error('Error checking auth status:', err);
      setError('Failed to check authentication status');
      setIsAuthenticated(false);
      setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: { username: string; password: string }) => {
    setLoading(true);
    setError(null);

    try {
      const result = await authService.login(credentials);
      authService.saveToken(result.access_token);

      setToken(result.access_token);
      setIsAuthenticated(true);
      // In a real app, you'd fetch user details here
      // setUser(fetchedUserDetails);
    } catch (err: any) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: { username: string; email: string; password: string }) => {
    setLoading(true);
    setError(null);

    try {
      const result = await authService.register(userData);
      authService.saveToken(result.access_token);

      setToken(result.access_token);
      setIsAuthenticated(true);
      // In a real app, you'd fetch user details here
      // setUser(fetchedUserDetails);
    } catch (err: any) {
      setError(err.message || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setToken(null);
    setUser(null);
    setError(null);
  };

  const value = {
    isAuthenticated,
    user,
    token,
    loading,
    error,
    login,
    register,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};