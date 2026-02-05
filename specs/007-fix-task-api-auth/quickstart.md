# Quickstart Guide: Fix Task API 401 Authentication & Migrate DB to Neon PostgreSQL

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL database (or Neon PostgreSQL account)
- Better Auth configured for JWT generation

## Environment Setup

1. **Database Configuration**
   ```bash
   # Create a .env file in backend directory
   cp backend/.env.example backend/.env

   # Update the DATABASE_URL to point to your PostgreSQL database
   DATABASE_URL="postgresql://username:password@host:port/database"

   # Ensure BETTER_AUTH_SECRET is set in both backend/.env and frontend environment
   BETTER_AUTH_SECRET="your-secret-key-here"
   ```

2. **Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install psycopg2-binary  # For PostgreSQL connectivity
   ```

3. **Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

## Database Migration

1. **Update Connection Configuration**
   - Modify `backend/src/database/connection.py` to use PostgreSQL
   - Ensure SQLAlchemy engine is configured with PostgreSQL dialect

2. **Test Database Connectivity**
   ```bash
   cd backend
   python -c "from src.database.connection import engine; print('Connected successfully')"
   ```

## JWT Authentication Setup

1. **Middleware Implementation**
   - Update `backend/src/auth/middleware.py` to validate JWT tokens
   - Ensure proper extraction from `Authorization: Bearer <token>` header
   - Verify token signature using `BETTER_AUTH_SECRET`

2. **API Route Protection**
   - Update task API endpoints to require valid JWT
   - Implement user ID enforcement (compare JWT user ID with route parameters)

## Running the Application

### Backend Development
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## Testing the Feature

1. **Verify JWT Authentication**
   - Login through the frontend to obtain JWT
   - Test API calls with valid JWT (should return 200/201)
   - Test API calls without JWT (should return 401)
   - Test API calls with invalid JWT (should return 401)
   - Test cross-user access (should return 403)

2. **Verify Database Migration**
   - Create tasks and verify they're stored in PostgreSQL
   - Restart the application and verify tasks persist
   - Check that no SQLite files are created

3. **API Endpoint Tests**
   ```bash
   # Test with curl or Postman
   curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
        -H "Content-Type: application/json" \
        http://localhost:8000/api/tasks/YOUR_USER_ID

   # Should return user's tasks
   ```

## Key Files to Modify

- `backend/src/auth/middleware.py` - JWT validation logic
- `backend/src/database/connection.py` - Database connection configuration
- `backend/src/api/tasks.py` - Task API endpoints with user enforcement
- `backend/src/main.py` - Main application setup with new middleware
- `frontend/src/services/api.ts` - API service with proper JWT handling

## Troubleshooting

**Issue**: Getting 401 errors even with valid JWT
- Verify the token is being sent in the `Authorization: Bearer <token>` header
- Check that `BETTER_AUTH_SECRET` matches between frontend and backend
- Ensure JWT is properly formatted and not expired

**Issue**: Database connection fails
- Verify `DATABASE_URL` is correctly formatted
- Check that PostgreSQL server is accessible
- Confirm credentials in the connection string are correct

**Issue**: Tasks don't persist after server restart
- Verify that the application is connecting to PostgreSQL, not SQLite
- Check that database tables are being created in the correct database