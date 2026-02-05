'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '../../../services/authService';
import { showToast } from "../../../components/Toast";
import { useAuth } from "../../../context/AuthContext";

interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

interface ErrorResponse {
  detail: string;
  errors?: ValidationError[];
}

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const router = useRouter();
  const { register } = useAuth();

  const clearFieldErrors = () => {
    setFieldErrors({});
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearFieldErrors();

    if (password !== confirmPassword) {
      showToast.error('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      // Use the AuthContext register method which handles token saving
      await register({ username, email, password });

      // Show success toast
      showToast.success("Registration successful! Redirecting to dashboard...");

      // Navigate to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      // Handle different types of errors from the backend
      if (err.response?.data) {
        const errorData: ErrorResponse = err.response.data;

        if (errorData.errors && Array.isArray(errorData.errors)) {
          // Handle validation errors from FastAPI
          const fieldErrorsMap: Record<string, string> = {};
          errorData.errors.forEach((validationError: ValidationError) => {
            // Extract field name from location (e.g., ['body', 'username'])
            const fieldName = validationError.loc[validationError.loc.length - 1];
            fieldErrorsMap[fieldName] = validationError.msg;
          });
          setFieldErrors(fieldErrorsMap);

          // Show error toast for field validation errors
          showToast.error('Please fix the errors below');
        } else if (errorData.detail) {
          // Handle specific error messages from backend
          showToast.error(errorData.detail);
        } else {
          showToast.error('Registration failed. Please try again.');
        }
      } else {
        const errorMessage = err.message || 'Registration failed. Please try again.';
        showToast.error(errorMessage);
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              if (fieldErrors.username) {
                setFieldErrors(prev => ({ ...prev, username: '' }));
              }
            }}
            className={fieldErrors.username ? 'error-border' : ''}
            required
            disabled={loading}
          />
          {fieldErrors.username && <span className="error-text">{fieldErrors.username}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (fieldErrors.email) {
                setFieldErrors(prev => ({ ...prev, email: '' }));
              }
            }}
            className={fieldErrors.email ? 'error-border' : ''}
            required
            disabled={loading}
          />
          {fieldErrors.email && <span className="error-text">{fieldErrors.email}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (fieldErrors.password) {
                setFieldErrors(prev => ({ ...prev, password: '' }));
              }
            }}
            className={fieldErrors.password ? 'error-border' : ''}
            required
            disabled={loading}
          />
          {fieldErrors.password && <span className="error-text">{fieldErrors.password}</span>}
        </div>
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirm Password:</label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p>
        Already have an account? <a href="/login">Login here</a>
      </p>
    </div>
  );
}