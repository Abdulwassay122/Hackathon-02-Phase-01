'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '../services/authService';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      // Add a small delay to ensure token is properly set before checking
      await new Promise(resolve => setTimeout(resolve, 100));

      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);

      if (!authenticated) {
        // Clear any potential invalid tokens
        authService.removeToken();
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Or a spinner component
  }

  if (!isAuthenticated) {
    return null; // The redirect happens in useEffect
  }

  return <>{children}</>;
}