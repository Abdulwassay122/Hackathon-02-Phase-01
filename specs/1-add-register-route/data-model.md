# Data Model: Registration Feature

## Entities

### User Registration Request
**Purpose**: Data structure for user registration input

**Fields**:
- username (string, required)
  - Min length: 3 characters
  - Max length: 50 characters
  - Pattern: alphanumeric with underscores/hyphens allowed
  - Must be unique across all users
- email (string, required)
  - Format: valid email address
  - Max length: 100 characters
  - Must be unique across all users
- password (string, required)
  - Min length: 8 characters
  - Should contain uppercase, lowercase, and special characters (recommended)

### User Registration Response
**Purpose**: Data structure returned after successful registration

**Fields**:
- access_token (string)
  - JWT token for authenticated session
  - Expires after 30 minutes (as per existing auth system)
- token_type (string)
  - Value: "bearer" (fixed)
- user (object)
  - id (string): unique user identifier
  - username (string): user's chosen username
  - email (string): user's email address
  - is_active (boolean): account activation status

### Registration Error Response
**Purpose**: Data structure for registration failure responses

**Fields**:
- detail (string)
  - Human-readable error message
  - Examples: "Username already exists", "Invalid email format"

## Relationships

### User Registration Request → User
- The registration request is validated and transformed into a User entity
- Password is hashed before creating the User entity
- Unique constraints are checked against existing User records

### User → User Registration Response
- Upon successful creation, User data is used to construct the response
- Access token is generated based on User information
- Sensitive data (password) is excluded from response

## Validation Rules

### Registration Request Validation
- All fields are required
- Username must be 3-50 alphanumeric characters plus underscores/hyphens
- Email must match standard email format
- Password must be at least 8 characters
- Username and email must be unique in the database

### Business Logic Validation
- Check for duplicate username in database
- Check for duplicate email in database
- Verify password meets security requirements

## State Transitions

### Registration Flow
1. Registration request received
2. Validation occurs (request format and business rules)
3. User entity created and persisted (if validation passes)
4. JWT token generated
5. Registration response returned to client

## Constraints

### Database Constraints
- User.username: UNIQUE constraint
- User.email: UNIQUE constraint
- User.username: NOT NULL, MAX_LENGTH 50
- User.email: NOT NULL, MAX_LENGTH 100
- User.password_hash: NOT NULL

### Application Constraints
- Password must be hashed before storing
- User is_active defaults to True upon registration
- Created timestamp is automatically set during registration