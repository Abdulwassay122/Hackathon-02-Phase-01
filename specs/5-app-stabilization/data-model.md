# Data Model: Application Stabilization and Full Functionality

## Authentication State Entity
- **name**: authenticationState
- **fields**:
  - isAuthenticated: boolean
  - user: User object (optional)
  - token: string (optional)
  - loading: boolean
  - error: string (optional)
- **relationships**: Connected to User entity for user details
- **validation rules**:
  - token must be present when isAuthenticated is true
  - user must be valid object when isAuthenticated is true
- **state transitions**:
  - unauthenticated → authenticating → authenticated/failed

## Toast Notification Entity
- **name**: toastNotification
- **fields**:
  - id: string (unique identifier)
  - message: string (notification text)
  - type: enum ['success', 'error', 'info', 'warning']
  - duration: number (milliseconds to display)
  - createdAt: timestamp
- **relationships**: Independent entity, may be triggered by various actions
- **validation rules**:
  - message must not be empty
  - type must be one of allowed values
  - duration must be positive number

## User Entity (existing)
- **name**: user
- **fields**:
  - id: string (primary key)
  - username: string
  - email: string
  - createdAt: timestamp
- **relationships**: Related to authentication state
- **validation rules**:
  - email must be valid format
  - username must be unique