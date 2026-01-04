# Claude Code Rules - Backend

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in backend development for the Todo App.

## Task context

**Your Surface:** You operate on the backend level, providing guidance to users and executing development tasks for the FastAPI backend.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Backend API follows REST principles
- Database operations are efficient and secure
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Backend follows FastAPI best practices
- SQLModel is used for database operations
- JWT authentication is properly implemented
- API endpoints are well-documented and secure
- All changes are small, testable, and reference code precisely.

## Development Guidelines

### 1. Backend Architecture:
- Use FastAPI for API development
- Implement SQLModel for database models
- Create services for business logic
- Use dependency injection where appropriate
- Follow REST API design principles

### 2. Database Operations:
- Use SQLModel for database models and operations
- Implement proper session management
- Add database indexes for performance
- Handle database transactions properly
- Implement proper error handling

### 3. Authentication & Authorization:
- Use JWT tokens for authentication
- Implement proper middleware for auth checks
- Ensure user data isolation
- Validate tokens properly
- Handle token refresh if needed

### 4. API Design:
- Follow REST conventions
- Implement proper HTTP status codes
- Use Pydantic models for request/response validation
- Document endpoints with OpenAPI/Swagger
- Handle errors consistently

### 5. Security:
- Validate all inputs
- Implement proper authorization checks
- Use parameterized queries to prevent SQL injection
- Protect against common vulnerabilities
- Sanitize user inputs where necessary

## Code Standards
- Follow Python PEP 8 standards
- Use type hints for all functions
- Write clear, descriptive function names
- Implement proper error handling
- Document public functions and classes