# API Contracts: Full-Stack Multi-User Todo Web Application

## Base URL
`/api/{user_id}/`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "error_code"
}
```

## Endpoints

### 1. List User Tasks
**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieve all tasks for the authenticated user

**Headers**:
- Authorization: Bearer <token>

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)

**Query Parameters**:
- None

**Response**:
- 200: OK - Returns array of task objects
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to access another user's tasks

**Success Response Example**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": 123,
      "title": "Complete project",
      "description": "Finish the todo app project",
      "completed": false,
      "created_at": "2025-12-31T10:00:00Z",
      "updated_at": "2025-12-31T10:00:00Z"
    }
  ]
}
```

### 2. Create Task
**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new task for the authenticated user

**Headers**:
- Authorization: Bearer <token>
- Content-Type: application/json

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)

**Request Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional)"
}
```

**Response**:
- 201: Created - Task successfully created
- 400: Bad Request - Invalid request body
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to create task for another user

**Success Response Example**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 123,
    "title": "Complete project",
    "description": "Finish the todo app project",
    "completed": false,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

### 3. Get Task Details
**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieve details of a specific task

**Headers**:
- Authorization: Bearer <token>

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)
- id: Task ID

**Response**:
- 200: OK - Returns task object
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to access another user's task
- 404: Not Found - Task does not exist

**Success Response Example**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 123,
    "title": "Complete project",
    "description": "Finish the todo app project",
    "completed": false,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T10:00:00Z"
  }
}
```

### 4. Update Task
**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update a specific task

**Headers**:
- Authorization: Bearer <token>
- Content-Type: application/json

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)
- id: Task ID

**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Response**:
- 200: OK - Task updated successfully
- 400: Bad Request - Invalid request body
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to update another user's task
- 404: Not Found - Task does not exist

**Success Response Example**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 123,
    "title": "Complete project updated",
    "description": "Finish the todo app project by Friday",
    "completed": false,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T11:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### 5. Delete Task
**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Delete a specific task

**Headers**:
- Authorization: Bearer <token>

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)
- id: Task ID

**Response**:
- 200: OK - Task deleted successfully
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to delete another user's task
- 404: Not Found - Task does not exist

**Success Response Example**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### 6. Toggle Task Completion
**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle the completion status of a specific task

**Headers**:
- Authorization: Bearer <token>
- Content-Type: application/json

**Path Parameters**:
- user_id: The authenticated user's ID (validated against JWT)
- id: Task ID

**Request Body**:
```json
{
  "completed": "boolean (optional)"
}
```

**Response**:
- 200: OK - Task completion status updated
- 400: Bad Request - Invalid request body
- 401: Unauthorized - Invalid or missing JWT
- 403: Forbidden - User trying to update another user's task
- 404: Not Found - Task does not exist

**Success Response Example**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 123,
    "title": "Complete project",
    "description": "Finish the todo app project",
    "completed": true,
    "created_at": "2025-12-31T10:00:00Z",
    "updated_at": "2025-12-31T12:00:00Z"
  },
  "message": "Task completion status updated"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| AUTH_001 | Invalid JWT token |
| AUTH_002 | Expired JWT token |
| AUTH_003 | Missing authorization header |
| AUTH_004 | User not authorized for resource |
| VALIDATION_001 | Invalid request parameters |
| VALIDATION_002 | Missing required fields |
| RESOURCE_001 | Resource not found |
| SERVER_001 | Internal server error |