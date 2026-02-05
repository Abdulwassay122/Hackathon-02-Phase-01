from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic import field_validator
import re

class TokenResponse(BaseModel):
    """Response model for authentication tokens"""
    access_token: str
    token_type: str = "bearer"
    user: dict

class LoginRequest(BaseModel):
    """Request model for login"""
    username: str
    password: str

class RegisterRequest(BaseModel):
    """Request model for user registration"""
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8)

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must contain only alphanumeric characters, underscores, and hyphens')
        return v

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(r'^[\w\.\+-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    """Response model for user information"""
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime