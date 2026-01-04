# Data Model: Backend Fixes & UI Enhancement

## Entities

### User
**Description**: Represents an authenticated user who can access the application
**Fields**:
- id (string/number): Unique identifier for the user
- username (string): User's identifier for login
- email (string): User's email address
- password_hash (string): Hashed password for authentication
- created_at (timestamp): Account creation timestamp
- updated_at (timestamp): Last update timestamp

### Authentication Token
**Description**: Represents a valid session token after successful login
**Fields**:
- token (string): JWT token string
- user_id (string/number): Reference to the user who owns this token
- expires_at (timestamp): Token expiration time
- created_at (timestamp): Token creation timestamp

### UI Components
**Description**: Represents the styled elements of the frontend application
**Fields**:
- component_name (string): Name of the UI component
- styling (object): Tailwind CSS classes and styling properties
- accessibility_props (object): ARIA attributes and accessibility features
- responsive_props (object): Responsive design properties for different screen sizes

## API Endpoints

### Authentication
- POST `/auth/login` - Authenticate user and return JWT token
- POST `/auth/logout` - Invalidate authentication token
- POST `/auth/refresh` - Refresh authentication token
- GET `/auth/me` - Get current user information

### Protected Task Management (with authentication required)
- GET `/api/tasks` - Retrieve all tasks for the authenticated user
- POST `/api/tasks` - Create a new task
- PUT `/api/tasks/{id}` - Update an existing task
- DELETE `/api/tasks/{id}` - Delete a task
- PATCH `/api/tasks/{id}/complete` - Toggle task completion status

### Expected Request/Response Formats

**Login Request**:
```json
{
  "username": "user123",
  "password": "user_password"
}
```

**Login Response**:
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "username": "user123"
  }
}
```

**Protected API Response (with Authorization header)**:
```json
{
  "id": "unique-id",
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

**Error Response**:
```json
{
  "detail": "Error message"
}
```