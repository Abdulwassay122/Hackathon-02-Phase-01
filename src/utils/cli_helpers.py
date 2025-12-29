"""
CLI helper functions for the Todo CLI application.

This module contains utility functions for input validation,
output formatting, and error message formatting.
"""

from typing import List
from models.task import Task


def format_task_list(tasks: List[Task]) -> str:
    """
    Format and display tasks in table format with ID, Title, Description, Status columns.

    Args:
        tasks (List[Task]): List of tasks to format

    Returns:
        str: Formatted table string
    """
    if not tasks:
        return "No tasks found"

    # Create header
    header = f"{'ID':<4} | {'Title':<20} | {'Description':<30} | {'Status':<12}"
    separator = "-" * len(header)

    # Create rows
    rows = [header, separator]
    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        description = task.description if task.description else ""
        # Truncate long titles and descriptions to fit the table
        title = task.title[:17] + "..." if len(task.title) > 17 else task.title
        desc = description[:27] + "..." if len(description) > 27 else description
        row = f"{task.id:<4} | {title:<20} | {desc:<30} | {status:<12}"
        rows.append(row)

    return "\n".join(rows)


def format_error_message(message: str) -> str:
    """
    Format error messages consistently.

    Args:
        message (str): The error message to format

    Returns:
        str: Formatted error message
    """
    return f"Error: {message}"


def validate_task_title(title: str) -> bool:
    """
    Validate that a task title is not empty.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if title is valid, False otherwise
    """
    return bool(title and title.strip())


def validate_task_id(task_id: str) -> bool:
    """
    Validate that a task ID is a positive integer.

    Args:
        task_id (str): The task ID to validate

    Returns:
        bool: True if task ID is valid, False otherwise
    """
    try:
        task_id_int = int(task_id)
        return task_id_int > 0
    except ValueError:
        return False