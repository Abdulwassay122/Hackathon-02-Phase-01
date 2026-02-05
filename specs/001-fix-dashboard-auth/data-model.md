# Data Model: Authentication State Management

## Overview
This document defines the data structures and relationships involved in managing authentication state for the dashboard access fix.

## Entities

### Authentication Token
**Purpose**: Represents a JWT token used for authenticating API requests

**Fields**:
- token (string)
  - The JWT token string
  - Format: Base64-encoded token with header.payload.signature structure
- expiration (datetime)
  - The time when the token expires
  - Used for determining if the token is still valid
- user_id (string)
  - The unique identifier of the user associated with the token
  - Retrieved from the token payload

**Relationships**:
- One-to-One: Associated with a User entity in the backend database
- One-to-Many: Multiple API requests may use the same token during its validity period

### Auth State (Frontend)
**Purpose**: Tracks the current authentication status in the frontend application

**Fields**:
- isAuthenticated (boolean)
  - Whether the user is currently authenticated
  - Determines access to protected routes
- user (object, optional)
  - User information retrieved from the token or API
  - May include username, email, etc.
- token (string, optional)
  - The current JWT token if authenticated
  - Stored in localStorage for persistence

**State Transitions**:
1. Initial State: isAuthenticated = false, user = null, token = null
2. Login Success: isAuthenticated = true, user = populated, token = valid JWT
3. Logout: isAuthenticated = false, user = null, token = null
4. Token Expiration: isAuthenticated = false, user = null, token = null

### User (Backend)
**Purpose**: Represents a registered user in the system

**Fields**:
- id (string)
  - Unique identifier for the user
- username (string)
  - Unique username for login
- email (string)
  - User's email address
- is_active (boolean)
  - Whether the account is active and can be used

**Relationships**:
- One-to-Many: Associated with multiple Authentication Tokens (over time)
- One-to-Many: Associated with multiple Tasks (via user_id foreign key)

## Validation Rules

### Token Validation
- Token must be a valid JWT format
- Token must not be expired (expiration > current time)
- Token signature must be valid and verifiable
- Token must correspond to an active user in the database

### Auth State Validation
- isAuthenticated can only be true if a valid token exists
- user information should be refreshed periodically to ensure accuracy
- Token should be cleared if validation fails

## State Transitions

### Authentication Flow
1. Unauthenticated State
   - User visits dashboard
   - System checks auth state
   - If not authenticated, redirects to login

2. Authentication Attempt
   - User provides credentials
   - System validates credentials against database
   - If valid, generates JWT token

3. Authenticated State
   - Token stored in frontend
   - Auth state updated to reflect authentication
   - User granted access to protected routes

4. Token Validation
   - On each protected route access
   - System validates token validity
   - If invalid, redirects to login

5. Logout
   - Token cleared from frontend
   - Auth state reset to unauthenticated
   - User redirected to login

## Constraints

### Backend Constraints
- User.username: UNIQUE, NOT NULL, VARCHAR(50)
- User.email: UNIQUE, NOT NULL, VARCHAR(100)
- User.is_active: BOOLEAN, DEFAULT true
- Token validation must occur for all protected endpoints

### Frontend Constraints
- Token must be stored securely (localStorage with proper security considerations)
- Auth state must be consistent across all components
- Redirect to login must occur immediately when authentication fails
- User experience must be seamless during authentication checks