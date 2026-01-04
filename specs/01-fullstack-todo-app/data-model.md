# Data Model: Full-Stack Multi-User Todo Web Application

## Entity: User
**Description**: Represents an authenticated user account managed by Better Auth system
**Attributes**:
- id: Unique identifier for the user (managed by Better Auth)
- email: User's email address (unique)
- name: User's display name
- created_at: Timestamp when user account was created
- updated_at: Timestamp when user account was last updated

**Relationships**:
- One-to-Many: A user can have many tasks

## Entity: Task
**Description**: Represents a todo item created by a user
**Attributes**:
- id: Unique identifier for the task (auto-generated)
- user_id: Foreign key linking to the user who owns this task
- title: Required string representing the task title
- description: Optional string with additional task details
- completed: Boolean indicating if the task is completed (default: false)
- created_at: Timestamp when task was created
- updated_at: Timestamp when task was last updated

**Validation Rules**:
- title is required and must not be empty
- user_id must reference an existing user
- completed defaults to false when creating a new task

**State Transitions**:
- New task: completed = false
- Toggle completion: completed = !completed
- Update task: attributes can be modified except id and user_id

## Database Schema

### Users Table (managed by Better Auth)
```
users
├── id (primary key)
├── email (unique, indexed)
├── name
├── created_at
└── updated_at
```

### Tasks Table
```
tasks
├── id (primary key)
├── user_id (foreign key to users)
├── title (not null)
├── description (nullable)
├── completed (boolean, default: false)
├── created_at
└── updated_at
```

## API Access Patterns
- Users can only access tasks where user_id matches their authenticated user ID
- All queries must be filtered by user_id to ensure data isolation
- Indexes should be created on user_id and created_at for efficient queries