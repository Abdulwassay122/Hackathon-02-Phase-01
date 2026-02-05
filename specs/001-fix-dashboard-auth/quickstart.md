# Quickstart Guide: Dashboard Authentication Fix

## Overview
This guide provides essential information for implementing the fix for 401 Unauthorized errors on the dashboard route. The solution involves adding frontend route protection to ensure only authenticated users can access the dashboard.

## Prerequisites
- Understanding of the existing authentication system (JWT-based with localStorage)
- Familiarity with Next.js App Router
- Knowledge of the existing authService and its methods
- Understanding of the current backend authentication middleware

## Frontend Implementation

### 1. Update Dashboard Page with Authentication Guard
Modify `frontend/src/app/dashboard/page.tsx` to check authentication status:

```typescript
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '../../services/authService';
import TodoList from '../../components/TodoList/TodoList';

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    if (!authService.isAuthenticated()) {
      // Redirect to login if not authenticated
      router.push('/login');
      // Optionally preserve the intended destination
      // router.push(`/login?redirect=/dashboard`);
    }
  }, [router]);

  // If not authenticated, don't render the dashboard content
  // The redirect will handle navigation
  if (!authService.isAuthenticated()) {
    return null; // Or a loading indicator while redirecting
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Todo Dashboard</h1>
        <TodoList />
      </div>
    </div>
  );
}
```

### 2. Alternative Approach: Server-Side Redirect
For better SEO and initial load performance, you could implement a server-side redirect in a layout file or by using Next.js server components:

```typescript
// In a server component or middleware
import { redirect } from 'next/navigation';
import { authService } from '../../services/authService';

async function checkAuthAndRedirect() {
  // Note: This approach would require server-side token validation
  // which may need additional setup for server-side JWT verification
  const isAuthenticated = authService.isAuthenticated(); // This won't work server-side

  if (!isAuthenticated) {
    redirect('/login');
  }
}
```

### 3. Enhanced Approach with Loading State
For better user experience, implement with loading state:

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '../../services/authService';
import TodoList from '../../components/TodoList/TodoList';

export default function Dashboard() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      // Small delay to ensure auth state is properly initialized
      await new Promise(resolve => setTimeout(resolve, 100));

      if (!authService.isAuthenticated()) {
        router.push('/login');
      }
      setIsLoading(false);
    };

    checkAuth();
  }, [router]);

  if (isLoading) {
    return <div>Loading...</div>; // Or your preferred loading component
  }

  if (!authService.isAuthenticated()) {
    return null; // Redirect is handled by useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Todo Dashboard</h1>
        <TodoList />
      </div>
    </div>
  );
}
```

## Backend Integration

### 1. Current Backend Protection
The backend already has proper authentication protection through the middleware system:
- All `/api/tasks` endpoints are protected by `get_current_user` dependency
- This ensures that even if someone bypasses frontend protection, API calls will fail

### 2. Token Validation
The backend's `src/auth/middleware.py` handles:
- JWT token extraction from Authorization header
- Token signature validation
- User existence verification
- User active status check

## Testing

### 1. Manual Testing
- Try accessing `/dashboard` without logging in → Should redirect to `/login`
- Log in, then access `/dashboard` → Should show dashboard
- Clear localStorage token, access `/dashboard` → Should redirect to `/login`
- Refresh dashboard page → Should remain accessible if authenticated

### 2. Edge Case Testing
- Test with expired tokens
- Test with malformed tokens
- Test behavior when localStorage is cleared mid-session
- Test simultaneous access from multiple tabs

## Security Considerations

### 1. Token Storage
- Current implementation uses localStorage (vulnerable to XSS)
- For enhanced security, consider HttpOnly cookies in the future

### 2. Client-Side Checks
- Frontend checks are for UX only
- Backend API endpoints must remain protected regardless

### 3. Redirect Preservation
Consider preserving the intended destination for post-login redirect:
```javascript
// When redirecting to login, preserve the intended destination
router.push(`/login?redirect=${encodeURIComponent(window.location.pathname)}`);
```

## Troubleshooting

### Common Issues
1. **Infinite Redirect Loop**: Ensure authService.isAuthenticated() doesn't have side effects
2. **Flash of Content**: Use loading states to prevent unauthenticated content from flashing
3. **Token Persistence**: Verify token is properly saved after login and cleared on logout

### Debugging Tips
- Check localStorage for 'access_token' presence
- Verify token format and expiration
- Monitor network requests to API endpoints for 401 responses
- Use browser dev tools to inspect auth state