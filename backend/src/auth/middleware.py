from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from src.utils.jwt import verify_jwt_token
from src.database.connection import get_session
import logging

# Configure logging
logger = logging.getLogger(__name__)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Get the current user from the Better Auth JWT token"""
    if not credentials:
        logger.warning("Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Use the new JWT utility to decode Better Auth tokens
        user_info = verify_jwt_token(token)
        user_id: str = user_info.get("user_id")

        if user_id is None:
            logger.warning("Token validation failed - missing user ID")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully authenticated user ID: {user_id}")
        return user_id  # Return user ID for authorization checks

    except HTTPException as e:
        # Re-raise HTTP exceptions as-is
        logger.warning(f"HTTP exception during token validation: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extract user ID directly from JWT token without database lookup
    This is used for enforcing user ownership without requiring database access
    """
    if not credentials:
        logger.warning("Authorization header missing in get_current_user_id_from_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    if not token or not isinstance(token, str):
        logger.warning("Invalid token in get_current_user_id_from_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_info = verify_jwt_token(token)
        user_id: str = user_info.get("user_id")

        if user_id is None:
            logger.warning("Token validation failed in get_current_user_id_from_token - missing user ID")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully extracted user ID from token: {user_id}")
        return user_id

    except HTTPException as e:
        # Re-raise HTTP exceptions as-is
        logger.warning(f"HTTP exception during token validation in get_current_user_id_from_token: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token validation in get_current_user_id_from_token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id_or_none(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get user ID from token if present, otherwise return None
    This is useful for checking if a user is authenticated without requiring authentication
    """
    if not credentials or not credentials.credentials:
        logger.debug("No authorization header provided in get_current_user_id_or_none")
        return None

    try:
        user_info = verify_jwt_token(credentials.credentials)
        user_id = user_info.get("user_id")
        logger.debug(f"Token validated successfully in get_current_user_id_or_none, user_id: {user_id}")
        return user_id
    except Exception as e:
        logger.warning(f"Token validation failed in get_current_user_id_or_none: {str(e)}")
        return None