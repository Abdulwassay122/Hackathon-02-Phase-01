# Quickstart Guide: Token Persistence Fix

## Setup Environment

1. Clone the repository and navigate to the project directory
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python -m src.main
   ```
2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## Key Files to Modify

### Frontend Changes
- `frontend/src/services/authService.ts` - Fix token storage and validation logic
- `frontend/src/context/AuthContext.tsx` - Improve authentication state management
- `frontend/src/components/ProtectedRoute.tsx` - Enhance authentication validation
- `frontend/src/app/(auth)/login/page.tsx` - Update redirect after login
- `frontend/src/app/dashboard/page.tsx` - Fix dashboard access and token persistence
- `frontend/src/services/api.ts` - Improve token handling in API calls

### Backend Changes
- `backend/src/auth/middleware.py` - Review authentication middleware
- `backend/src/api/auth.py` - Ensure proper response formats

## Testing the Changes

1. Login with valid credentials and verify token persists after dashboard redirect
2. Refresh dashboard page and verify continued authentication
3. Manually clear token and verify redirect to login page
4. Test API calls with and without valid tokens
5. Verify proper error handling for invalid/expired tokens