"""
Task service layer for the Todo CLI application.

This module contains the TaskService class that provides business logic
for task operations, acting as an interface between the CLI and the data layer.
"""

from typing import List, Optional
from models.task import Task, TaskCollection


class TaskService:
    """
    Business logic layer for task operations.
    """

    def __init__(self):
        """
        Initialize the TaskService with a TaskCollection.
        """
        self.collection = TaskCollection()

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task with title validation.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            ValueError: If title is empty or None
        """
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        return self.collection.add_task(title, description)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        return self.collection.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List[Task]: A list of all tasks, sorted by ID
        """
        return self.collection.get_all_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update task with validation.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if task was updated, False if task not found

        Raises:
            ValueError: If title is provided but is empty
        """
        # Validate title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")

        return self.collection.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task with existence check.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        return self.collection.delete_task(task_id)

    def toggle_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if task status was toggled, False if task not found
        """
        return self.collection.toggle_completion(task_id)