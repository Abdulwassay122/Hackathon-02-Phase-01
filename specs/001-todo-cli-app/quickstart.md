# Quickstart Guide: In-Memory Python Todo CLI App

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
python src/main.py [command] [options]
```

## Basic Usage

### Add a New Task

To add a task with just a title:
```bash
python src/main.py add --title "Buy groceries"
```

To add a task with both title and description:
```bash
python src/main.py add --title "Finish project" --description "Complete the final report"
```

### View All Tasks

To see all your tasks:
```bash
python src/main.py list
```

This will display a table with ID, Title, Description, and Status columns.

### Update a Task

To update a task's title:
```bash
python src/main.py update --id 1 --title "Updated task title"
```

To update a task's description:
```bash
python src/main.py update --id 1 --description "New description for the task"
```

To update both title and description:
```bash
python src/main.py update --id 1 --title "New title" --description "New description"
```

### Delete a Task

To delete a task:
```bash
python src/main.py delete --id 1
```

### Mark Task Complete/Incomplete

To toggle a task's completion status:
```bash
python src/main.py complete --id 1
```

If the task was incomplete, it will be marked as complete. If it was complete, it will be marked as incomplete.

## Example Workflow

Here's a complete example of using the application:

```bash
# Add a few tasks
python src/main.py add --title "Buy groceries" --description "Milk, eggs, bread"
python src/main.py add --title "Finish report"
python src/main.py add --title "Call doctor"

# View all tasks
python src/main.py list

# Update a task
python src/main.py update --id 2 --description "Complete the quarterly report"

# Mark a task as complete
python src/main.py complete --id 1

# Delete a task
python src/main.py delete --id 3

# View tasks again to see changes
python src/main.py list
```

## Getting Help

To see all available commands and options:
```bash
python src/main.py --help
```

## Error Handling

The application handles errors gracefully:

- Invalid commands will show a helpful error message
- Missing required arguments will prompt for the necessary information
- Non-existent task IDs will return an appropriate error message
- Empty titles will be rejected with an explanation

## Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs are automatically assigned and are unique within a single session
- The application follows all specified requirements for functionality and error handling