from sqlmodel import Session, select
from src.models.user import User
from src.utils.password import verify_password, hash_password
from src.utils.jwt import create_access_token
from src.models.auth_response import TokenResponse, UserResponse
from datetime import timedelta
from typing import Optional

class AuthService:
    """Service class for authentication operations"""

    @staticmethod
    def authenticate_user(session: Session, username: str, password: str) -> Optional[TokenResponse]:
        """Authenticate a user and return a token response"""
        # Find user by username
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        # Check if user exists and password is correct
        if not user or not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        # Create access token
        access_token_expires = timedelta(minutes=30)  # 30 minutes expiry
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )

        # Create token response
        token_response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
        )

        return token_response

    @staticmethod
    def create_user(session: Session, username: str, email: str, password: str) -> User:
        """Create a new user with hashed password"""
        hashed_password = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user