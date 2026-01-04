from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Index

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: str

class Task(TaskBase, table=True):
    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_completed", "completed"),
        Index("idx_user_completed", "user_id", "completed"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime