# Todo API Documentation

## Base URL
`http://localhost:8000/api` (development) or your deployed URL

## Authentication
All endpoints (except health check) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Health Check
- `GET /health` - Check API health status
- `GET /ready` - Check API readiness

### Task Management

#### Get User Tasks
- `GET /users/{user_id}/tasks`
- Returns: Array of Task objects
- Requires: Valid JWT token matching user_id

#### Create Task
- `POST /users/{user_id}/tasks`
- Body: TaskCreate object
- Returns: Created Task object
- Requires: Valid JWT token matching user_id

#### Get Single Task
- `GET /users/{user_id}/tasks/{task_id}`
- Returns: Task object
- Requires: Valid JWT token matching user_id

#### Update Task
- `PUT /users/{user_id}/tasks/{task_id}`
- Body: TaskUpdate object
- Returns: Updated Task object
- Requires: Valid JWT token matching user_id

#### Delete Task
- `DELETE /users/{user_id}/tasks/{task_id}`
- Returns: Success message
- Requires: Valid JWT token matching user_id

#### Toggle Task Completion
- `PATCH /users/{user_id}/tasks/{task_id}/complete`
- Returns: Updated Task object with completion status
- Requires: Valid JWT token matching user_id

## Data Models

### Task
```
{
  "id": number,
  "title": string,
  "description": string | null,
  "completed": boolean,
  "user_id": number,
  "created_at": string (ISO date),
  "updated_at": string (ISO date)
}
```

### TaskCreate
```
{
  "title": string,
  "description": string (optional),
  "completed": boolean (default: false)
}
```

### TaskUpdate
```
{
  "title": string (optional),
  "description": string (optional),
  "completed": boolean (optional)
}
```