# In-Memory Python Todo CLI App

A simple command-line todo application built in Python with in-memory storage.

## Features

- Add new tasks with required title and optional description
- View all tasks with ID, title, description, and completion status
- Update task title and/or description using task ID
- Delete tasks using task ID
- Toggle task completion status using task ID
- All data stored in memory only (no persistent storage)
- Comprehensive error handling and validation
- Formatted table output for better readability
- Full command-line interface with help documentation

## Prerequisites

- Python 3.13+

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Ensure Python 3.13+ is installed and available

## Usage

### Add a New Task
```bash
python src/main.py add --title "Task Title" [--description "Task Description"]
```

Examples:
```bash
# Add a task with title only
python src/main.py add --title "Buy groceries"

# Add a task with title and description
python src/main.py add --title "Finish project" --description "Complete the final report"
```

### View All Tasks
```bash
python src/main.py list
```

This will display a table with ID, Title, Description, and Status columns.

### Update a Task
```bash
python src/main.py update --id ID [--title "New Title"] [--description "New Description"]
```

Examples:
```bash
# Update a task's title
python src/main.py update --id 1 --title "Updated task title"

# Update a task's description
python src/main.py update --id 1 --description "New description for the task"

# Update both title and description
python src/main.py update --id 1 --title "New title" --description "New description"
```

### Delete a Task
```bash
python src/main.py delete --id ID
```

Example:
```bash
python src/main.py delete --id 1
```

### Mark Task Complete/Incomplete
```bash
python src/main.py complete --id ID
```

Example:
```bash
python src/main.py complete --id 1
```

If the task was incomplete, it will be marked as complete. If it was complete, it will be marked as incomplete.

### Getting Help
```bash
# Show general help
python src/main.py --help

# Show help for a specific command
python src/main.py add --help
python src/main.py list --help
python src/main.py update --help
python src/main.py delete --help
python src/main.py complete --help
```

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

## Error Handling

The application handles errors gracefully:

- Invalid commands will show a helpful error message
- Missing required arguments will prompt for the necessary information
- Non-existent task IDs will return an appropriate error message
- Empty titles will be rejected with an explanation
- Invalid argument types (e.g., non-integer IDs) will be caught and reported

## Architecture

The application follows a clean architecture pattern:

- **Models**: Task and TaskCollection classes manage data and business logic
- **Services**: TaskService provides a clean interface for task operations
- **Utils**: CLI helpers provide formatting and validation utilities
- **Main**: Command-line interface and argument parsing

## Testing

The application includes comprehensive test coverage:

- Unit tests for model classes
- Integration tests for service layer
- Contract tests for CLI interface
- End-to-end functionality tests

Run the tests using Python's unittest module:
```bash
# Run all unit tests
python -m unittest discover -s tests/unit -v

# Run all integration tests
python -m unittest discover -s tests/integration -v

# Run all contract tests
python -m unittest discover -s tests/contract -v
```

## Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs are automatically assigned and are unique within a single session
- The application follows all specified requirements for functionality and error handling
- All code follows PEP 8 standards for Python code style