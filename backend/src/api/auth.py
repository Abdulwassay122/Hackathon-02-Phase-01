from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database.connection import get_session
from src.models.auth_response import LoginRequest, TokenResponse, UserResponse
from src.services.auth_service import AuthService
from src.auth.middleware import get_current_user as get_current_user_from_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token"""
    token_response = AuthService.authenticate_user(
        session, login_request.username, login_request.password
    )

    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_response

@router.post("/logout")
def logout():
    """Invalidate authentication token (client-side only)"""
    # In a real implementation, you might want to add tokens to a blacklist
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user(current_user_id: str = Depends(get_current_user_from_token), session: Session = Depends(get_session)):
    """Get current user information"""
    # Get the full user details from the database using the user ID from the token
    from backend.src.models.user import User
    from sqlmodel import select

    statement = select(User).where(User.id == current_user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )