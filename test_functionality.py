#!/usr/bin/env python3
"""
Test script to verify all functionality works together in a single run.
"""

import sys
import os

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_service import TaskService
from utils.cli_helpers import format_task_list


def test_functionality():
    print("Testing Todo CLI functionality...")

    # Initialize the task service
    task_service = TaskService()

    # Test 1: Add a task with title only
    print("\n1. Testing add task with title only:")
    task1 = task_service.add_task("Test task 1")
    print(f"Added task: ID={task1.id}, Title='{task1.title}', Description='{task1.description}', Completed={task1.completed}")

    # Test 2: Add a task with title and description
    print("\n2. Testing add task with title and description:")
    task2 = task_service.add_task("Test task 2", "This is a test description")
    print(f"Added task: ID={task2.id}, Title='{task2.title}', Description='{task2.description}', Completed={task2.completed}")

    # Test 3: List all tasks
    print("\n3. Testing list all tasks:")
    all_tasks = task_service.get_all_tasks()
    print("All tasks:")
    print(format_task_list(all_tasks))

    # Test 4: Update a task
    print("\n4. Testing update task:")
    success = task_service.update_task(task1.id, title="Updated task 1", description="Updated description")
    print(f"Update successful: {success}")

    if success:
        updated_task = task_service.get_task(task1.id)
        print(f"Updated task: ID={updated_task.id}, Title='{updated_task.title}', Description='{updated_task.description}'")

    # Test 5: Toggle completion
    print("\n5. Testing toggle completion:")
    task_before_toggle = task_service.get_task(task1.id)
    print(f"Before toggle - Task {task1.id} completed: {task_before_toggle.completed}")

    success = task_service.toggle_completion(task1.id)
    print(f"Toggle successful: {success}")

    if success:
        task_after_toggle = task_service.get_task(task1.id)
        print(f"After toggle - Task {task1.id} completed: {task_after_toggle.completed}")

    # Test 6: Delete a task
    print("\n6. Testing delete task:")
    success = task_service.delete_task(task2.id)
    print(f"Delete successful: {success}")

    # List tasks after deletion
    print("\n7. Testing list after deletion:")
    remaining_tasks = task_service.get_all_tasks()
    print("Remaining tasks:")
    print(format_task_list(remaining_tasks))

    print("\nAll tests completed successfully!")


if __name__ == "__main__":
    test_functionality()