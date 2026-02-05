import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import TaskService
from src.auth.middleware import get_current_user_id_from_token
from src.database.connection import get_session

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks/{user_id}", response_model=dict)
async def get_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(get_current_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for a user
    Verify that the authenticated user ID matches the requested user ID
    """
    logger.info(f"User {authenticated_user_id} requesting tasks for user {user_id}")

    if authenticated_user_id != user_id:
        logger.warning(f"Access denied: User {authenticated_user_id} attempted to access tasks for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only access your own tasks"
        )

    try:
        task_service = TaskService(session)
        tasks = task_service.get_tasks(user_id)
        logger.info(f"Successfully retrieved {len(tasks)} tasks for user {user_id}")
        return {"tasks": tasks}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving tasks"
        )

@router.post("/tasks/{user_id}", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task: TaskCreate,
    authenticated_user_id: str = Depends(get_current_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    Verify that the user_id in the path matches the authenticated user
    """
    logger.info(f"User {authenticated_user_id} attempting to create task for user {user_id}")

    if authenticated_user_id != user_id:
        logger.warning(f"Access denied: User {authenticated_user_id} attempted to create task for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only create tasks for yourself"
        )

    try:
        # Override user_id to ensure the task belongs to the authenticated user
        task_with_user = task.model_copy(update={"user_id": user_id})

        task_service = TaskService(session)
        created_task = task_service.create_task(task_with_user)
        logger.info(f"Successfully created task {created_task.id} for user {user_id}")
        return created_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the task"
        )

@router.get("/tasks/{user_id}/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    authenticated_user_id: str = Depends(get_current_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task
    Verify that the authenticated user ID matches the requested user ID
    """
    logger.info(f"User {authenticated_user_id} requesting task {task_id} for user {user_id}")

    if authenticated_user_id != user_id:
        logger.warning(f"Access denied: User {authenticated_user_id} attempted to access task {task_id} for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only access your own tasks"
        )

    try:
        task_service = TaskService(session)
        task = task_service.get_task(task_id, user_id)
        logger.info(f"Successfully retrieved task {task_id} for user {user_id}")
        return task
    except PermissionError:
        logger.warning(f"Permission denied: User {user_id} tried to access unauthorized task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only access your own tasks"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the task"
        )

@router.put("/tasks/{user_id}/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    authenticated_user_id: str = Depends(get_current_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Update an existing task
    Verify that the authenticated user ID matches the requested user ID
    """
    logger.info(f"User {authenticated_user_id} attempting to update task {task_id} for user {user_id}")

    if authenticated_user_id != user_id:
        logger.warning(f"Access denied: User {authenticated_user_id} attempted to update task {task_id} for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only update your own tasks"
        )

    try:
        task_service = TaskService(session)
        updated_task = task_service.update_task(task_id, task_update, user_id)
        logger.info(f"Successfully updated task {task_id} for user {user_id}")
        return updated_task
    except PermissionError:
        logger.warning(f"Permission denied: User {user_id} tried to update unauthorized task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only update your own tasks"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the task"
        )

@router.delete("/tasks/{user_id}/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    authenticated_user_id: str = Depends(get_current_user_id_from_token),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task
    Verify that the authenticated user ID matches the requested user ID
    """
    logger.info(f"User {authenticated_user_id} attempting to delete task {task_id} for user {user_id}")

    if authenticated_user_id != user_id:
        logger.warning(f"Access denied: User {authenticated_user_id} attempted to delete task {task_id} for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only delete your own tasks"
        )

    try:
        task_service = TaskService(session)
        task_service.delete_task(task_id, user_id)
        logger.info(f"Successfully deleted task {task_id} for user {user_id}")
    except PermissionError:
        logger.warning(f"Permission denied: User {user_id} tried to delete unauthorized task {task_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only delete your own tasks"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the task"
        )

# Optional: Keep the original routes for backward compatibility if needed
# Or remove them if they conflict with the new API structure