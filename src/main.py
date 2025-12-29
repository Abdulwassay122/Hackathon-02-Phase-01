#!/usr/bin/env python3
"""
Main entry point for the Interactive Menu-Driven Todo CLI Application.

This module implements an interactive menu-driven interface for the todo application
with numbered options 1-6 that guide users through different operations.
"""

import sys
import os
from services.task_service import TaskService
from utils.cli_helpers import format_task_list, format_error_message


def display_menu():
    """Display the main menu with numbered options."""
    print("\n===== TODO APPLICATION =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Mark task complete/incomplete")
    print("6. Exit")
    print("============================")


def get_menu_choice():
    """Get and validate menu choice from user."""
    try:
        choice = input("Enter your choice (1-6): ").strip()

        # Validate numeric input
        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1-6.")
            return None

        choice_num = int(choice)

        # Validate range
        if choice_num < 1 or choice_num > 6:
            print("Invalid selection. Please enter a number between 1-6.")
            return None

        return choice_num
    except (EOFError, KeyboardInterrupt):
        print("\nApplication interrupted. Exiting...")
        return 6  # Treat as exit choice


def handle_add_task(task_service):
    """Handle adding a new task."""
    try:
        title = input("Enter task title: ").strip()

        if not title:
            print(format_error_message("Title is required and cannot be empty"))
            return

        description_input = input("Enter task description (optional): ").strip()
        description = description_input if description_input else None

        task = task_service.add_task(title, description)
        print(f"Task added successfully with ID: {task.id}")

    except (EOFError, KeyboardInterrupt):
        print("\nOperation interrupted.")
    except ValueError as e:
        print(format_error_message(str(e)))
    except Exception as e:
        print(format_error_message(f"An error occurred: {str(e)}"))


def handle_view_tasks(task_service):
    """Handle viewing all tasks."""
    try:
        tasks = task_service.get_all_tasks()
        print(format_task_list(tasks))
    except Exception as e:
        print(format_error_message(f"An error occurred: {str(e)}"))


def handle_update_task(task_service):
    """Handle updating a task."""
    try:
        task_id_input = input("Enter task ID to update: ").strip()

        if not task_id_input.isdigit():
            print(format_error_message("Invalid input. Please enter a valid task ID."))
            return

        task_id = int(task_id_input)

        # Check if task exists
        task = task_service.get_task(task_id)
        if not task:
            print(format_error_message(f"Task with ID {task_id} not found"))
            return

        # Get new title (optional)
        current_title = task.title
        new_title_input = input(f"Enter new title (or press Enter to keep '{current_title}'): ").strip()
        new_title = new_title_input if new_title_input else None

        # Get new description (optional)
        current_description = task.description if task.description else ""
        new_description_input = input(f"Enter new description (or press Enter to keep '{current_description}'): ").strip()
        new_description = new_description_input if new_description_input != "" else None

        # Update the task
        success = task_service.update_task(task_id, new_title, new_description)

        if success:
            print(f"Task {task_id} updated successfully")
        else:
            print(format_error_message(f"Task with ID {task_id} not found"))

    except (EOFError, KeyboardInterrupt):
        print("\nOperation interrupted.")
    except ValueError as e:
        print(format_error_message(str(e)))
    except Exception as e:
        print(format_error_message(f"An error occurred: {str(e)}"))


def handle_delete_task(task_service):
    """Handle deleting a task."""
    try:
        task_id_input = input("Enter task ID to delete: ").strip()

        if not task_id_input.isdigit():
            print(format_error_message("Invalid input. Please enter a valid task ID."))
            return

        task_id = int(task_id_input)

        # Check if task exists
        task = task_service.get_task(task_id)
        if not task:
            print(format_error_message(f"Task with ID {task_id} not found"))
            return

        success = task_service.delete_task(task_id)

        if success:
            print(f"Task {task_id} deleted successfully")
        else:
            print(format_error_message(f"Task with ID {task_id} not found"))

    except (EOFError, KeyboardInterrupt):
        print("\nOperation interrupted.")
    except ValueError as e:
        print(format_error_message(str(e)))
    except Exception as e:
        print(format_error_message(f"An error occurred: {str(e)}"))


def handle_toggle_completion(task_service):
    """Handle toggling task completion status."""
    try:
        task_id_input = input("Enter task ID to toggle completion status: ").strip()

        if not task_id_input.isdigit():
            print(format_error_message("Invalid input. Please enter a valid task ID."))
            return

        task_id = int(task_id_input)

        # Check if task exists
        task = task_service.get_task(task_id)
        if not task:
            print(format_error_message(f"Task with ID {task_id} not found"))
            return

        success = task_service.toggle_completion(task_id)

        if success:
            updated_task = task_service.get_task(task_id)
            status = "complete" if updated_task.completed else "incomplete"
            print(f"Task {task_id} marked as {status}")
        else:
            print(format_error_message(f"Task with ID {task_id} not found"))

    except (EOFError, KeyboardInterrupt):
        print("\nOperation interrupted.")
    except ValueError as e:
        print(format_error_message(str(e)))
    except Exception as e:
        print(format_error_message(f"An error occurred: {str(e)}"))


def main():
    """Main entry point for the menu-driven application."""
    # Add the src directory to the path to allow imports from the project root
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Initialize the task service
    task_service = TaskService()

    print("Welcome to the Todo Application!")

    while True:
        try:
            display_menu()
            choice = get_menu_choice()

            if choice is None:
                # Invalid input, continue to show menu again
                continue

            if choice == 1:
                handle_add_task(task_service)
            elif choice == 2:
                handle_view_tasks(task_service)
            elif choice == 3:
                handle_update_task(task_service)
            elif choice == 4:
                handle_delete_task(task_service)
            elif choice == 5:
                handle_toggle_completion(task_service)
            elif choice == 6:
                print("Thank you for using the Todo Application. Goodbye!")
                break

        except (EOFError, KeyboardInterrupt):
            print("\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            print(format_error_message(f"An unexpected error occurred: {str(e)}"))
            print("Returning to main menu...")


if __name__ == '__main__':
    main()