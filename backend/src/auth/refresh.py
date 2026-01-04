from datetime import timedelta
from typing import Optional
from jose import JWTError, jwt
from src.config import settings
from src.auth.jwt import create_access_token

def create_refresh_token(data: dict):
    """
    Create a refresh token with a longer expiration time
    """
    expire = timedelta(days=7)  # Refresh tokens last 7 days
    return create_access_token(data, expire)

def verify_refresh_token(token: str):
    """
    Verify a refresh token (same logic as access token but for refresh tokens)
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None