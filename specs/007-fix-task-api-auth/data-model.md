# Data Model: Fix Task API 401 Authentication & Migrate DB to Neon PostgreSQL

## Entity Definitions

### JWT Token
- **Description**: Authentication token containing user identity information
- **Fields**:
  - `token` (string): Encoded JWT token string
  - `user_id` (string): Unique identifier of the authenticated user
  - `email` (string): User's email address (optional)
  - `exp` (integer): Expiration timestamp
  - `iat` (integer): Issued at timestamp
- **Relationships**: Associates authenticated user with API requests
- **Validation Rules**: Must be signed with `BETTER_AUTH_SECRET`, must not be expired

### Task
- **Description**: Individual task item owned by a specific user
- **Fields**:
  - `id` (integer): Unique identifier for the task
  - `title` (string): Title or description of the task
  - `description` (string): Detailed description of the task
  - `completed` (boolean): Whether the task is completed
  - `user_id` (string): ID of the user who owns this task
  - `created_at` (datetime): Timestamp when task was created
  - `updated_at` (datetime): Timestamp when task was last updated
- **Relationships**: Belongs to one User (via user_id foreign key)
- **Validation Rules**:
  - user_id must match the authenticated user's ID from JWT
  - title must not be empty
  - user_id cannot be changed after creation

### User
- **Description**: Identity associated with JWT token and task ownership
- **Fields**:
  - `id` (string): Unique identifier for the user
  - `email` (string): User's email address
  - `created_at` (datetime): Timestamp when user account was created
- **Relationships**: Owns many Tasks
- **Validation Rules**:
  - id must match the user_id in JWT tokens
  - email must be a valid email format

## State Transitions

### Task State Transitions
- **Initial State**: New task created with `completed = false`
- **Complete**: `completed` changes from `false` to `true`
- **Reopen**: `completed` changes from `true` to `false`
- **Delete**: Task record removed from database

## Database Schema (SQLModel)

```python
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Request/Response Models

### JWT Validation Result
- `user_id`: String containing validated user ID from JWT
- `valid`: Boolean indicating if JWT is valid
- `error`: String error message if validation failed

### Task API Request Models
- `CreateTaskRequest`:
  - `title`: String
  - `description`: Optional string
  - `user_id`: String (derived from JWT, not from request body)

- `UpdateTaskRequest`:
  - `title`: Optional string
  - `description`: Optional string
  - `completed`: Optional boolean

### Task API Response Models
- `TaskResponse`:
  - `id`: Integer
  - `title`: String
  - `description`: Optional string
  - `completed`: Boolean
  - `user_id`: String
  - `created_at`: ISO datetime string
  - `updated_at`: ISO datetime string

- `TaskListResponse`:
  - `tasks`: Array of TaskResponse objects