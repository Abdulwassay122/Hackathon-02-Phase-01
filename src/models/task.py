"""
Task model and collection for the Todo CLI application.

This module contains the Task class representing a single todo item
and the TaskCollection class for managing multiple tasks.
"""

from typing import Dict, List, Optional


class Task:
    """
    Represents a single todo task with id, title, description, and completion status.
    """

    def __init__(self, task_id: int, title: str, description: Optional[str] = None):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Required title of the task
            description (str, optional): Optional description of the task
        """
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip() if description else None
        self.completed = False  # Default to False as per requirements


class TaskCollection:
    """
    A container for managing multiple Task entities with O(1) lookup performance.
    """

    def __init__(self):
        """
        Initialize an empty TaskCollection with a counter for unique IDs.
        """
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create new Task with unique ID and add to collection.

        Args:
            title (str): Required title of the task
            description (str, optional): Optional description of the task

        Returns:
            Task: The newly created task with assigned ID
        """
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        task_id = self.next_id
        self.next_id += 1

        task = Task(task_id, title, description)
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update specified task attributes.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if task was updated, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Validate title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else None

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove task from collection.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_all_tasks(self) -> List[Task]:
        """
        Return all tasks in the collection.

        Returns:
            List[Task]: A list of all tasks, sorted by ID
        """
        return sorted(self.tasks.values(), key=lambda x: x.id)

    def toggle_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if task status was toggled, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.completed = not task.completed
        return True