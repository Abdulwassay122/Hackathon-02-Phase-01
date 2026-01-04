'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const isAuthenticated = typeof window !== 'undefined' && localStorage.getItem('access_token') !== null;

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <div className="md:hidden">
      <button
        onClick={toggleMenu}
        className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 focus:outline-none"
      >
        <svg
          className={`${isOpen ? 'hidden' : 'block'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg
          className={`${isOpen ? 'block' : 'hidden'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white shadow-lg rounded-md">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className={`block px-3 py-2 rounded-md ${pathname === '/dashboard' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  onClick={closeMenu}
                >
                  Dashboard
                </Link>
                <Link
                  href="/profile"
                  className={`block px-3 py-2 rounded-md ${pathname === '/profile' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  onClick={closeMenu}
                >
                  Profile
                </Link>
                <button
                  onClick={() => {
                    localStorage.removeItem('access_token');
                    window.location.href = '/login';
                    closeMenu();
                  }}
                  className="block w-full text-left px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className={`block px-3 py-2 rounded-md ${pathname === '/login' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  onClick={closeMenu}
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className={`block px-3 py-2 rounded-md ${pathname === '/register' ? 'bg-indigo-100 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}
                  onClick={closeMenu}
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}