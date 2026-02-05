# Quickstart Guide: Full-Stack Integration, Tailwind Fix, and UI Stabilization

**Feature**: Full-Stack Integration, Tailwind Fix, and UI Stabilization
**Branch**: `4-fullstack-stabilization`
**Created**: 2026-01-04

## Overview

This quickstart guide provides the essential steps to get the full-stack integrated Todo application running with proper Tailwind CSS styling and stable UI components. This guide is intended for developers who need to quickly set up and run the application after the stabilization work is complete.

## Prerequisites

### System Requirements
- **Node.js**: Version 18.x or higher
- **Python**: Version 3.10 or higher
- **uv**: Python package manager (or pip/poetry)
- **Git**: Version control system
- **SQLite**: Database (typically bundled with Python)

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   git checkout 4-fullstack-stabilization
   ```

2. Install Python dependencies:
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r backend/requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Environment Variables

Create `.env` files in both frontend and backend directories:

### Backend (.env)
```env
DATABASE_URL=sqlite:///./todo.db
BETTER_AUTH_SECRET=your-super-secret-key-here
BETTER_AUTH_URL=http://localhost:8000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:8000
```

## Running the Application

### Development Mode

#### Option 1: Separate Terminals
1. Terminal 1 - Start Backend:
   ```bash
   cd backend
   uv run main.py
   # Server will run on http://localhost:8000
   ```

2. Terminal 2 - Start Frontend:
   ```bash
   cd frontend
   npm run dev
   # Server will run on http://localhost:3000
   ```

#### Option 2: Using Docker (if available)
```bash
docker-compose up --build
```

### Production Mode
```bash
# Build frontend
cd frontend
npm run build

# Start both services
cd ..
uv run backend/main.py
```

## Key Integration Points

### 1. API Communication
- **Frontend API Service**: Located at `frontend/src/services/api.ts`
- **Base URL**: Configured via `NEXT_PUBLIC_API_URL` environment variable
- **Authentication**: JWT tokens automatically attached to requests
- **Error Handling**: Global 401 handling redirects to login

### 2. Authentication Flow
1. User logs in via authentication endpoint
2. JWT token is stored in browser storage
3. Token is automatically attached to all authenticated requests
4. 401 responses trigger automatic logout and redirect to login

### 3. Tailwind CSS Configuration
- **Configuration File**: `frontend/tailwind.config.ts`
- **CSS File**: `frontend/src/app/globals.css` (contains @tailwind directives)
- **Layout File**: `frontend/src/app/layout.tsx` (imports global CSS)

## Troubleshooting Common Issues

### 1. Tailwind CSS Not Applying
**Symptoms**: Components appear unstyled or with default browser styles
**Solutions**:
- Verify `tailwind.config.ts` content paths include all component files
- Ensure `@tailwind base;`, `@tailwind components;`, and `@tailwind utilities;` exist in globals.css
- Restart development server after configuration changes
- Check that global CSS is imported in layout.tsx

### 2. API Communication Errors
**Symptoms**: Network errors, 404s, or CORS issues
**Solutions**:
- Verify backend server is running on configured port
- Check that `NEXT_PUBLIC_API_URL` matches backend server URL
- Verify CORS configuration allows frontend origin
- Ensure authentication token is properly set for protected endpoints

### 3. Authentication Issues
**Symptoms**: 401 errors, inability to access protected routes
**Solutions**:
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check JWT token format and validity
- Ensure authentication endpoints are accessible
- Verify token is properly stored and attached to requests

### 4. Database Connection Issues
**Symptoms**: 500 errors, inability to save/load data
**Solutions**:
- Verify `DATABASE_URL` environment variable is set correctly
- Check that SQLite database file has proper permissions
- Ensure database migrations are applied
- Verify SQLModel configuration is correct

## Verification Steps

### 1. Backend Verification
1. Visit `http://localhost:8000` - should show FastAPI docs
2. Visit `http://localhost:8000/docs` - should show API documentation
3. Test `/api/health` endpoint - should return health status

### 2. Frontend Verification
1. Visit `http://localhost:3000` - should load the application
2. Check browser console for no errors
3. Verify Tailwind styles are applied (proper spacing, colors, etc.)

### 3. Integration Verification
1. Create a test user account
2. Log in to the application
3. Create a test task
4. Verify task appears in the list with proper styling
5. Update and delete the task to verify full CRUD functionality

## Development Workflow

### Frontend Development
```bash
cd frontend
npm run dev
# Visit http://localhost:3000
```

### Backend Development
```bash
cd backend
uv run main.py
# Visit http://localhost:8000/docs for API docs
```

### Testing
```bash
# Run backend tests
cd backend
uv run pytest

# Run frontend tests
cd frontend
npm run test

# Run integration tests (if available)
python -m pytest tests/integration/
```

## Key Files and Directories

### Frontend
- `frontend/src/services/api.ts` - API client with authentication
- `frontend/src/app/layout.tsx` - Root layout with CSS imports
- `frontend/src/app/globals.css` - Global styles with Tailwind directives
- `frontend/tailwind.config.ts` - Tailwind configuration
- `frontend/src/components/` - Reusable UI components

### Backend
- `backend/main.py` - FastAPI application entry point
- `backend/api/` - API route definitions
- `backend/models/` - SQLModel database models
- `backend/schemas/` - Pydantic request/response schemas
- `backend/auth/` - Authentication middleware and services

## Environment Configuration

### Development Environment
```env
# Backend
DATABASE_URL=sqlite:///./todo_dev.db
BETTER_AUTH_SECRET=dev-secret-key-change-in-production
BETTER_AUTH_URL=http://localhost:8000
DEBUG=true

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_DEBUG=true
```

### Production Environment
```env
# Backend
DATABASE_URL=postgresql://user:password@host:port/database
BETTER_AUTH_SECRET=production-secret-key
BETTER_AUTH_URL=https://api.yourdomain.com

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_AUTH_URL=https://api.yourdomain.com
```

## Next Steps

1. **Customize**: Modify components to match your design requirements
2. **Extend**: Add additional features while maintaining integration patterns
3. **Deploy**: Set up CI/CD pipeline for automated deployment
4. **Monitor**: Implement logging and monitoring for production use