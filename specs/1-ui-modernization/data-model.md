# Data Model: UI Modernization & Backend UV Environment

## Entities

### Task
**Description**: Represents a user's to-do item
**Fields**:
- id (string/number): Unique identifier for the task
- title (string): Task title (required)
- description (string): Optional task description
- completed (boolean): Completion status (default: false)
- createdAt (timestamp): Creation timestamp
- updatedAt (timestamp): Last update timestamp

**Validation Rules**:
- title must be present and non-empty
- id must be unique within the system
- createdAt and updatedAt are automatically managed

**State Transitions**:
- New task: completed = false (default)
- Mark complete: completed = true
- Mark incomplete: completed = false

### User (Existing)
**Description**: Represents an authenticated user who can manage tasks
**Fields**:
- id (string/number): Unique identifier for the user
- username (string): User's identifier
- tasks (array): Collection of user's tasks

**Relationships**:
- One User to Many Tasks (user owns multiple tasks)

## API Endpoints

### Task Management
- GET `/api/tasks` - Retrieve all tasks for the authenticated user
- POST `/api/tasks` - Create a new task
- PUT `/api/tasks/{id}` - Update an existing task
- DELETE `/api/tasks/{id}` - Delete a task
- PATCH `/api/tasks/{id}/complete` - Mark task as complete/incomplete

### Expected Request/Response Formats

**Create Task Request**:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Task Response**:
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

**Update Task Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Toggle Complete Request**:
```json
{
  "completed": true
}
```