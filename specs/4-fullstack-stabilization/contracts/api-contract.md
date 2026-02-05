# API Contract: Full-Stack Integration, Tailwind Fix, and UI Stabilization

**Feature**: Full-Stack Integration, Tailwind Fix, and UI Stabilization
**Branch**: `4-fullstack-stabilization`
**Created**: 2026-01-04

## Overview

This contract defines the API interfaces between the frontend and backend for the Todo application. It specifies the endpoints, request/response formats, authentication requirements, and error handling patterns that must be maintained during the full-stack integration and stabilization process.

## Authentication Contract

### JWT Token Requirements
- **Header**: `Authorization: Bearer {token}`
- **Token Format**: JWT with `sub` (user ID), `email`, `iat`, and `exp` claims
- **Token Storage**: Frontend stores in browser storage (localStorage/cookie)
- **Token Refresh**: Not required for development (long-lived tokens)

### Authentication Endpoints
```
POST /api/auth/login
- Request: { email: string, password: string }
- Response: { success: boolean, data: { token: string, user: User }, error?: string }
- Status: 200 (success), 401 (invalid credentials)

GET /api/auth/me
- Headers: Authorization: Bearer {token}
- Response: { success: boolean, data: User, error?: string }
- Status: 200 (success), 401 (unauthorized)

POST /api/auth/logout
- Headers: Authorization: Bearer {token}
- Response: { success: boolean, message: string, error?: string }
- Status: 200 (success), 401 (unauthorized)
```

## Task API Contract

### Get All Tasks
```
GET /api/tasks
- Headers: Authorization: Bearer {token}
- Query Parameters: None
- Response: { success: boolean, data: Task[], error?: string }
- Status: 200 (success), 401 (unauthorized), 500 (server error)
- Example Response:
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "title": "Sample task",
        "description": "Task description",
        "completed": false,
        "user_id": "user-uuid",
        "created_at": "2026-01-04T21:00:00.000Z",
        "updated_at": "2026-01-04T21:00:00.000Z"
      }
    ]
  }
```

### Create Task
```
POST /api/tasks
- Headers: Authorization: Bearer {token}, Content-Type: application/json
- Body: { title: string, description?: string }
- Response: { success: boolean, data: Task, error?: string }
- Status: 201 (created), 400 (validation error), 401 (unauthorized), 500 (server error)
- Example Request:
  {
    "title": "New task",
    "description": "Task description"
  }
- Example Response:
  {
    "success": true,
    "data": {
      "id": 2,
      "title": "New task",
      "description": "Task description",
      "completed": false,
      "user_id": "user-uuid",
      "created_at": "2026-01-04T21:00:00.000Z",
      "updated_at": "2026-01-04T21:00:00.000Z"
    }
  }
```

### Update Task
```
PUT /api/tasks/{id}
- Headers: Authorization: Bearer {token}, Content-Type: application/json
- Path: id (task ID)
- Body: { title?: string, description?: string, completed?: boolean }
- Response: { success: boolean, data: Task, error?: string }
- Status: 200 (updated), 400 (validation error), 401 (unauthorized), 404 (not found), 500 (server error)
- Example Request:
  {
    "title": "Updated task title",
    "completed": true
  }
- Example Response:
  {
    "success": true,
    "data": {
      "id": 2,
      "title": "Updated task title",
      "description": "Task description",
      "completed": true,
      "user_id": "user-uuid",
      "created_at": "2026-01-04T21:00:00.000Z",
      "updated_at": "2026-01-04T21:01:00.000Z"
    }
  }
```

### Delete Task
```
DELETE /api/tasks/{id}
- Headers: Authorization: Bearer {token}
- Path: id (task ID)
- Response: { success: boolean, error?: string }
- Status: 200 (deleted), 401 (unauthorized), 404 (not found), 500 (server error)
- Example Response:
  {
    "success": true
  }
```

## Error Response Format

All error responses follow the same format:

```
{
  "success": false,
  "error": "Error message",
  "message": "Human-readable error description"
}
```

### Common Error Types
- **400 Bad Request**: Validation errors (invalid input data)
- **401 Unauthorized**: Missing or invalid authentication token
- **404 Not Found**: Requested resource does not exist
- **500 Server Error**: Internal server error

## Frontend API Client Contract

### API Service Interface
```typescript
interface ApiService {
  get<T>(url: string): Promise<ApiResponse<T>>;
  post<T, R>(url: string, data: T): Promise<ApiResponse<R>>;
  put<T, R>(url: string, data: T): Promise<ApiResponse<R>>;
  delete<T>(url: string): Promise<ApiResponse<T>>;
  setAuthToken(token: string): void;
  clearAuthToken(): void;
}
```

### Authentication Handling
- **Token Storage**: Service should handle JWT token storage and retrieval
- **Request Interception**: Automatically attach Authorization header to authenticated requests
- **Response Interception**: Handle 401 responses globally and redirect to login

### Error Handling Contract
- **Network Errors**: Catch and return structured error responses
- **401 Handling**: Clear authentication and redirect to login page
- **User Feedback**: Provide user-friendly error messages
- **Retry Logic**: Implement retry logic for transient network failures

## Frontend Component Data Contract

### Task Management Components
- **TaskList**: Receives array of Task objects, handles loading/error states
- **TaskForm**: Accepts Task object for editing, returns Task object on submission
- **TaskItem**: Displays single Task object, handles individual actions

### Loading States
- **Initial Load**: Show loading spinner when fetching tasks
- **Action States**: Show loading indicators during create/update/delete operations
- **Error States**: Show user-friendly error messages with retry options

## Performance Contract

### Response Time Requirements
- **API Response Time**: 95% of requests should respond within 2 seconds
- **Frontend Rendering**: UI updates should be immediate after API responses
- **Caching**: Implement appropriate caching for repeated requests

### Resource Usage
- **Bundle Size**: Keep frontend bundle under 250KB
- **Memory Usage**: Avoid memory leaks in component lifecycle
- **Network Efficiency**: Batch operations when possible

## Security Contract

### Data Validation
- **Frontend**: Validate user input before sending to backend
- **Backend**: Validate all data before processing or storage
- **Format Validation**: Ensure data types match expected formats

### Authentication Flow
- **Token Management**: Securely store and handle JWT tokens
- **Session Management**: Implement proper session lifecycle
- **Token Expiration**: Handle token expiration gracefully

## Integration Contract

### CORS Configuration
- **Allowed Origins**: Frontend URL must be allowed in CORS settings
- **Allowed Methods**: GET, POST, PUT, DELETE for API endpoints
- **Allowed Headers**: Authorization, Content-Type, and other required headers

### Environment Configuration
- **API Base URL**: Configurable through environment variables
- **Authentication URL**: Separate authentication service URL if needed
- **Development/Production**: Different configurations for different environments

## Testing Contract

### API Testing Requirements
- **Unit Tests**: Individual endpoint testing
- **Integration Tests**: Full request/response cycle testing
- **Authentication Tests**: Token handling and validation testing

### Frontend Testing Requirements
- **Component Tests**: Individual component functionality
- **Integration Tests**: API client integration
- **End-to-End Tests**: Complete user workflows

## Versioning Contract

### API Versioning
- **Current Version**: No explicit versioning (v1 implied)
- **Backward Compatibility**: Maintain contract during stabilization phase
- **Breaking Changes**: Require new API version for breaking changes

### Contract Maintenance
- **Documentation Updates**: Update contract when API changes
- **Frontend Alignment**: Ensure frontend adapts to API contract changes
- **Testing Updates**: Update tests when contract changes