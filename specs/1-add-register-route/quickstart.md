# Quickstart Guide: Registration Feature Implementation

## Overview
This guide provides the essential information for implementing the user registration feature, including the backend API endpoint and frontend integration.

## Prerequisites
- Understanding of the existing authentication system
- Familiarity with FastAPI and Next.js
- Knowledge of the existing User model and AuthService

## Backend Implementation

### 1. Create Registration Request Model
Add a new model to `backend/src/models/auth_response.py`:
```python
class RegisterRequest(BaseModel):
    """Request model for user registration"""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(min_length=8)
```

### 2. Add Registration Endpoint
In `backend/src/api/auth.py`, add:
```python
@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(register_request: RegisterRequest, session: Session = Depends(get_session)):
    """Register a new user and return JWT token"""
    # Check if username or email already exists
    existing_user_by_username = session.exec(select(User).where(User.username == register_request.username)).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    existing_user_by_email = session.exec(select(User).where(User.email == register_request.email)).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Create new user using AuthService
    user = AuthService.create_user(
        session,
        register_request.username,
        register_request.email,
        register_request.password
    )

    # Authenticate the new user and return token (similar to login)
    token_response = AuthService.authenticate_user(session, register_request.username, register_request.password)
    return token_response
```

### 3. Import Required Classes
Make sure to add the necessary imports to the auth.py file.

## Frontend Implementation

### 1. Update AuthService
Modify `frontend/src/services/authService.ts`:
```typescript
async register(userData: RegisterData): Promise<AuthResponse> {
  // Call the backend API
  const response = await apiService.post<AuthResponse>('/auth/register', userData);
  return response;
}
```

### 2. Update Register Page
Modify `frontend/src/app/(auth)/register/page.tsx` to call the real service:
```typescript
try {
  const result = await authService.register({ username, email, password });
  authService.saveToken(result.access_token);

  router.push('/dashboard');
  router.refresh();
} catch (err: any) {
  setError(err.message || 'Registration failed. Please try again.');
  console.error(err);
}
```

## Testing

### Backend Tests
- Test successful registration with valid data
- Test duplicate username handling
- Test duplicate email handling
- Test validation for invalid data

### Frontend Tests
- Test successful registration flow
- Test error handling for duplicate accounts
- Test validation error display

## Security Considerations
- Passwords are automatically hashed by the AuthService
- Input validation prevents injection attacks
- Proper error messages don't reveal if accounts already exist

## Error Handling
- 201: Successful registration
- 400: Invalid input data
- 409: Username or email already exists
- 422: Validation errors