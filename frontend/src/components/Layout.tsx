'use client';

import { ReactNode } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname();
  const isAuthenticated = typeof window !== 'undefined' && localStorage.getItem('access_token') !== null;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold text-indigo-600">
                Todo App
              </Link>
            </div>
            <nav className="flex items-center space-x-4">
              {isAuthenticated ? (
                <>
                  <Link
                    href="/dashboard"
                    className={`px-3 py-2 rounded-md ${pathname === '/dashboard' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/profile"
                    className={`px-3 py-2 rounded-md ${pathname === '/profile' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  >
                    Profile
                  </Link>
                  <button
                    onClick={() => {
                      localStorage.removeItem('access_token');
                      window.location.href = '/login';
                    }}
                    className="px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-md"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className={`px-3 py-2 rounded-md ${pathname === '/login' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  >
                    Login
                  </Link>
                  <Link
                    href="/register"
                    className={`px-3 py-2 rounded-md ${pathname === '/register' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  >
                    Register
                  </Link>
                </>
              )}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>

      <footer className="bg-white mt-8 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500">
            © {new Date().getFullYear()} Todo App. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}