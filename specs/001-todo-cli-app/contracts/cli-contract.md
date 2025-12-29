# CLI Contract: In-Memory Python Todo CLI App

## Command Structure

The application follows the pattern: `python todo.py [command] [options]`

## Commands

### 1. Add Task
**Command**: `python todo.py add --title "Task Title" [--description "Task Description"]`

**Input Parameters**:
- `--title` (required): String representing the task title (non-empty)
- `--description` (optional): String providing additional task details

**Success Response**:
- Task created with unique ID
- Success message: "Task added successfully with ID: {id}"

**Error Responses**:
- Invalid input: "Error: Title is required and cannot be empty"
- Other errors: Appropriate error message

### 2. List Tasks
**Command**: `python todo.py list`

**Input Parameters**: None

**Success Response**:
- Formatted list of all tasks with columns: ID, Title, Description, Status
- Example format:
```
ID  | Title              | Description        | Status
----|--------------------|--------------------|--------
1   | Buy groceries      | Get milk and eggs  | Incomplete
2   | Finish report      |                    | Complete
```

**Error Responses**:
- If no tasks: "No tasks found"

### 3. Update Task
**Command**: `python todo.py update --id ID [--title "New Title"] [--description "New Description"]`

**Input Parameters**:
- `--id` (required): Integer ID of the task to update
- `--title` (optional): New title for the task
- `--description` (optional): New description for the task

**Success Response**:
- Success message: "Task {id} updated successfully"

**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"
- Invalid input: "Error: Title cannot be empty"

### 4. Delete Task
**Command**: `python todo.py delete --id ID`

**Input Parameters**:
- `--id` (required): Integer ID of the task to delete

**Success Response**:
- Success message: "Task {id} deleted successfully"

**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"

### 5. Complete Task
**Command**: `python todo.py complete --id ID`

**Input Parameters**:
- `--id` (required): Integer ID of the task to mark complete/incomplete

**Success Response**:
- Success message: "Task {id} marked as {status}" (where status is "complete" or "incomplete")

**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"

## Common Error Responses

- **Invalid command**: "Error: Invalid command. Use 'python todo.py --help' for usage information"
- **Missing required argument**: "Error: Missing required argument --{arg}"
- **Invalid argument type**: "Error: Invalid value for --{arg}: {value} is not a valid {type}"
- **General error**: "An error occurred: {error_message}"