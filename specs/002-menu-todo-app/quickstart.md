# Quickstart Guide: Interactive Menu-Driven Todo CLI App

## Prerequisites

- Python 3.13+ installed on your system
- Command-line access (Terminal on macOS/Linux, Command Prompt or PowerShell on Windows)

## Setup

1. Clone or download the repository containing the todo application
2. Navigate to the project directory
3. Ensure you're using Python 3.13+ (check with `python --version`)

## Running the Application

The application is run directly as a Python script:

```bash
python src/main.py
```

## Basic Usage

When the application starts, you'll see a numbered menu with the following options:

```
===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6):
```

### Add a New Task
1. Select option `1` from the menu
2. Enter the task title when prompted
3. Optionally enter a description when prompted
4. The system will confirm the task was added with its ID
5. You'll be returned to the main menu

### View All Tasks
1. Select option `2` from the menu
2. All tasks will be displayed in a table format with ID, Title, Description, and Status
3. You'll be returned to the main menu

### Update a Task
1. Select option `3` from the menu
2. Enter the task ID when prompted
3. Enter the new title (or press Enter to keep current)
4. Enter the new description (or press Enter to keep current)
5. The system will confirm the update
6. You'll be returned to the main menu

### Delete a Task
1. Select option `4` from the menu
2. Enter the task ID when prompted
3. The system will confirm the deletion
4. You'll be returned to the main menu

### Mark Task Complete/Incomplete
1. Select option `5` from the menu
2. Enter the task ID when prompted
3. The system will toggle the completion status and confirm
4. You'll be returned to the main menu

### Exit the Application
1. Select option `6` from the menu
2. The application will terminate cleanly

## Example Workflow

Here's a complete example of using the application:

```
===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully with ID: 1

===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 1
Enter task title: Finish report
Task added successfully with ID: 2

===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 2
ID  | Title              | Description        | Status
----|--------------------|--------------------|--------
1   | Buy groceries      | Milk, eggs, bread  | Incomplete
2   | Finish report      |                    | Incomplete

===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 5
Enter task ID to toggle completion status: 1
Task 1 marked as complete

===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 2
ID  | Title              | Description        | Status
----|--------------------|--------------------|--------
1   | Buy groceries      | Milk, eggs, bread  | Complete
2   | Finish report      |                    | Incomplete

===== TODO APPLICATION =====
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Mark task complete/incomplete
6. Exit
============================
Enter your choice (1-6): 6
```

## Error Handling

The application handles errors gracefully:

- Invalid menu selections will prompt for valid input (1-6)
- Missing required information will prompt again
- Non-existent task IDs will return an appropriate error message
- Empty titles will be rejected with an explanation
- Invalid input types will be caught and handled appropriately

## Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs are automatically assigned and are unique within a single session
- The application follows all specified requirements for functionality and error handling
- Each operation returns to the main menu after completion (success or failure)