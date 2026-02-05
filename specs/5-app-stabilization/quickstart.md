# Quickstart Guide: Application Stabilization

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
- `frontend/src/components/ProtectedRoute.tsx` - Fix dashboard access control
- `frontend/src/app/(auth)/login/page.tsx` - Add toast notifications
- `frontend/src/app/(auth)/register/page.tsx` - Add toast notifications
- `frontend/src/services/authService.ts` - Enhance authentication handling
- `frontend/src/app/dashboard/page.tsx` - Verify access control

### Backend Changes
- `backend/src/auth/middleware.py` - Review authentication middleware
- `backend/src/api/auth.py` - Ensure proper response formats for toast messages

## Testing the Changes

1. Login with valid credentials and verify dashboard access
2. Attempt login with invalid credentials and verify error toast
3. Register with valid data and verify success toast
4. Register with invalid data and verify error toast
5. Refresh dashboard page and verify continued access