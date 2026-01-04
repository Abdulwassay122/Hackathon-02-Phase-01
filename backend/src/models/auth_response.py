from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenResponse(BaseModel):
    """Response model for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    user: dict

class LoginRequest(BaseModel):
    """Request model for login"""
    username: str
    password: str

class UserResponse(BaseModel):
    """Response model for user information"""
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime