from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService
from src.auth.middleware import get_current_user
from src.database.connection import get_session

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user  # Assuming current_user is the user ID

    task_service = TaskService(session)
    tasks = task_service.get_tasks(user_id)
    return tasks

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user  # Assuming current_user is the user ID

    # Override user_id to ensure the task belongs to the authenticated user
    task_with_user = task.model_copy(update={"user_id": user_id})

    task_service = TaskService(session)
    created_task = task_service.create_task(task_with_user)
    return created_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user  # Assuming current_user is the user ID

    task_service = TaskService(session)
    updated_task = task_service.update_task(task_id, task_update, user_id)
    return updated_task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user  # Assuming current_user is the user ID

    task_service = TaskService(session)
    task_service.delete_task(task_id, user_id)
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete")
async def toggle_task_completion(task_id: int, current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user_id = current_user  # Assuming current_user is the user ID

    task_service = TaskService(session)
    updated_task = task_service.toggle_task_completion(task_id, user_id)
    return {"task": updated_task, "message": "Task completion status updated"}