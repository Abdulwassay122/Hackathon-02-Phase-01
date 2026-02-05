from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database.connection import get_session
from src.models.auth_response import LoginRequest, TokenResponse, UserResponse, RegisterRequest
from src.models.user import User
from src.services.auth_service import AuthService
from src.auth.middleware import get_current_user as get_current_user_from_token
from datetime import timedelta
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token"""
    try:
        logger.info(f"Login attempt for user: {login_request.username}")

        token_response = AuthService.authenticate_user(
            session, login_request.username, login_request.password
        )

        if not token_response:
            logger.warning(f"Failed login attempt for user: {login_request.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successful login for user: {login_request.username}")
        return token_response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )

@router.post("/logout")
def logout():
    """Invalidate authentication token (client-side only)"""
    # In a real implementation, you might want to add tokens to a blacklist
    # For now, we'll just return a success message
    logger.info("User logout requested")
    return {"message": "Successfully logged out"}

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(register_request: RegisterRequest, session: Session = Depends(get_session)):
    """Register a new user and return JWT token"""
    try:
        logger.info(f"Registration request for username: {register_request.username}, email: {register_request.email}")

        # Check if username or email already exists
        existing_user_by_username = session.exec(select(User).where(User.username == register_request.username)).first()
        if existing_user_by_username:
            logger.warning(f"Registration failed: Username already exists: {register_request.username}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

        existing_user_by_email = session.exec(select(User).where(User.email == register_request.email)).first()
        if existing_user_by_email:
            logger.warning(f"Registration failed: Email already exists: {register_request.email}")
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

        logger.info(f"User created successfully: {user.id}")

        # Authenticate the new user and return token (similar to login)
        token_response = AuthService.authenticate_user(session, register_request.username, register_request.password)
        if not token_response:
            logger.error(f"Registration succeeded but authentication failed for user: {register_request.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Registration failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successful registration and authentication for user: {register_request.username}")
        return token_response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user(current_user_id: str = Depends(get_current_user_from_token), session: Session = Depends(get_session)):
    """Get current user information"""
    try:
        logger.info(f"Getting user information for user ID: {current_user_id}")

        # Get the full user details from the database using the user ID from the token
        statement = select(User).where(User.id == current_user_id)
        user = session.exec(statement).first()

        if not user:
            logger.warning(f"User not found for ID: {current_user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"Successfully retrieved user information for user ID: {current_user_id}")
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving user information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving user information"
        )