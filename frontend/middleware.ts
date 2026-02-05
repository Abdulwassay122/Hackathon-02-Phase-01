import { NextRequest, NextResponse } from 'next/server';

// Protect dashboard and other authenticated routes
export function middleware(request: NextRequest) {
  // Get the token from cookies or headers
  const token = request.cookies.get('token')?.value || request.headers.get('Authorization')?.replace('Bearer ', '');

  // Define protected routes
  const protectedPaths = ['/dashboard', '/profile', '/settings'];
  const currentPath = request.nextUrl.pathname;

  // Check if the current path is protected
  const isProtected = protectedPaths.some(path =>
    currentPath.startsWith(path)
  );

  // If accessing a protected route without authentication, redirect to login
  if (isProtected && !token) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Apply middleware to specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
    // Specifically include protected routes
    '/dashboard/:path*',
    '/profile/:path*',
    '/settings/:path*',
  ],
};