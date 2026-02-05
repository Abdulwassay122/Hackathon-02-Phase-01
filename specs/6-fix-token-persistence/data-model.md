# Data Model: Token Persistence and Authentication Flow Fix

## Authentication Token Entity
- **name**: authenticationToken
- **fields**:
  - token: string (JWT token value)
  - expiration: timestamp (when token expires)
  - createdAt: timestamp (when token was created)
  - isValid: boolean (whether token is currently valid)
  - userId: string (optional, user identifier)
- **relationships**: Connected to User entity for user details
- **validation rules**:
  - token must be valid JWT format
  - expiration must be in the future when valid
  - createdAt must be before expiration time
- **state transitions**:
  - pending → valid → expired/invalid

## Token Validator Entity
- **name**: tokenValidator
- **fields**:
  - token: string (reference to authentication token)
  - validationResult: enum ['valid', 'expired', 'invalid', 'missing']
  - lastValidated: timestamp
  - error: string (optional, reason for invalidation)
- **relationships**: Connected to authenticationToken entity
- **validation rules**:
  - validationResult must be one of allowed values
  - lastValidated must be recent for current validation
- **state transitions**:
  - not_validated → validating → [valid, expired, invalid, missing]

## Authentication Fallback Entity (existing)
- **name**: authenticationFallback
- **fields**:
  - redirectUrl: string (where to redirect on auth failure)
  - cleanupActions: array (actions to perform on invalid auth)
  - timestamp: timestamp
- **relationships**: Triggered by invalid authenticationToken
- **validation rules**:
  - redirectUrl must be valid application route
  - cleanupActions must be valid authentication cleanup operations