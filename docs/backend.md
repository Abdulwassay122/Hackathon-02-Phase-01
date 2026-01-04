# Backend Documentation

## Project Structure
```
backend/
├── src/
│   ├── models/        # SQLModel database models
│   ├── services/      # Business logic services
│   ├── api/           # API route definitions
│   ├── auth/          # Authentication and authorization
│   ├── database/      # Database connection and setup
│   └── utils/         # Utility functions
├── migrations/        # Database migration scripts
├── scripts/           # Utility scripts
├── tests/             # Test files
├── requirements.txt   # Python dependencies
└── .env              # Environment variables
```

## Core Components

### Database Models
- `Task` - Core task model with SQLModel
- Relations defined with proper constraints

### Services
- `TaskService` - Business logic for task operations
- Session-based database transactions

### API Routes
- `/api/tasks` - Task management endpoints
- `/api/health` - Health check endpoints
- JWT token validation on all secured routes

### Authentication
- JWT-based authentication
- Token creation and validation utilities
- Authentication middleware
- Authorization checks

## Database

### Connection
- PostgreSQL with SQLModel
- Connection pooling configured
- Environment-based configuration

### Migrations
- Alembic-ready migration structure
- Initial schema migration script

## Environment Variables
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

## Running the Application

### Development
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Database Setup
```bash
python scripts/seed_db.py
```