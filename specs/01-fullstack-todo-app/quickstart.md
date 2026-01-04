# Quickstart Guide: Full-Stack Todo Application

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL (or Neon Serverless PostgreSQL account)
- Git

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (FastAPI)

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] python-multipart psycopg2-binary
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database connection details and JWT secret
```

5. Run database migrations:
```bash
# This would be implemented in a migration script
```

6. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)

1. Navigate to frontend directory:
```bash
cd frontend  # from project root
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit with your backend API URL and auth configuration
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

### 4. Application Structure

```
project-root/
├── backend/
│   ├── src/
│   │   ├── models/      # SQLModel definitions
│   │   ├── services/    # Business logic
│   │   ├── api/         # API routes
│   │   └── auth/        # Authentication utilities
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Next.js pages
│   │   ├── services/    # API service functions
│   │   └── lib/         # Utility functions
│   └── tests/
└── specs/               # Specification files
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret (same as backend)
```

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

## API Endpoints

Backend runs on `http://localhost:8000`
- GET `/api/{user_id}/tasks` - List user's tasks
- POST `/api/{user_id}/tasks` - Create new task
- GET `/api/{user_id}/tasks/{id}` - Get specific task
- PUT `/api/{user_id}/tasks/{id}` - Update task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

## Authentication Flow

1. User registers/logs in via Better Auth on frontend
2. JWT token is stored securely in browser
3. Token is automatically attached to all API requests
4. Backend validates JWT and verifies user ownership of resources