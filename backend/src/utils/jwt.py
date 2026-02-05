from datetime import datetime, timedelta
from typing import Optional
import jwt
from src.config import settings
from fastapi import HTTPException, status
from jose import JWTError
import logging

# Configure logging
logger = logging.getLogger(__name__)


def decode_better_auth_token(token: str):
    """
    Decode and validate JWT token from Better Auth
    """
    if not settings.better_auth_secret:
        logger.error("Better Auth secret not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Better Auth secret not configured"
        )

    # Validate token format
    if not token or not isinstance(token, str):
        logger.warning("Invalid token format: token is None or not a string")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Basic format check (JWT should have 3 parts separated by dots)
    token_parts = token.split('.')
    if len(token_parts) != 3:
        logger.warning(f"Invalid JWT format: token does not have 3 parts - received {len(token_parts)} parts")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the token using the better auth secret
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        user_id: str = payload.get("userId")
        email: str = payload.get("email")

        if user_id is None:
            logger.warning("Token payload missing user ID")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successfully decoded token for user ID: {user_id}")
        return {
            "user_id": user_id,
            "email": email
        }

    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidSignatureError:
        logger.warning("Invalid token signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.DecodeError:
        logger.warning("Token could not be decoded - invalid format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode token - invalid format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError:
        logger.warning("Invalid token claims")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"JWT error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_jwt_token(token: str):
    """
    Verify JWT token and return user information
    """
    return decode_better_auth_token(token)
