from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AuthToken(SQLModel, table=True):
    """Authentication token model for session management"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    token: str = Field(unique=True)
    user_id: str = Field(foreign_key="user.id")
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<AuthToken(id={self.id}, user_id={self.user_id})>"