# CLI Contract: Interactive Menu-Driven Todo CLI App

## Menu Interface

The application presents an interactive menu-driven interface with the following options:

### Menu Options
1. **Add task**: Add a new task with required title and optional description
2. **View tasks**: Display all tasks in a readable format
3. **Update task**: Modify title and/or description of an existing task
4. **Delete task**: Remove a task by its ID
5. **Mark task complete/incomplete**: Toggle the completion status of a task
6. **Exit**: Terminate the application cleanly

## Command Flows

### 1. Add Task Flow
**Prompt**: "Enter task title: "
**Optional Prompt**: "Enter task description (optional): "
**Success Response**: "Task added successfully with ID: {id}"
**Error Responses**:
- Invalid input: "Error: Title is required and cannot be empty"
- Other errors: Appropriate error message

### 2. View Tasks Flow
**Input**: None (immediate display)
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

### 3. Update Task Flow
**Prompt**: "Enter task ID to update: "
**Prompt**: "Enter new title (or press Enter to keep current): "
**Prompt**: "Enter new description (or press Enter to keep current): "
**Success Response**: "Task {id} updated successfully"
**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"
- Invalid input: "Error: Title cannot be empty"

### 4. Delete Task Flow
**Prompt**: "Enter task ID to delete: "
**Success Response**: "Task {id} deleted successfully"
**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"

### 5. Mark Complete/Incomplete Flow
**Prompt**: "Enter task ID to toggle completion status: "
**Success Response**: "Task {id} marked as {status}" (where status is "complete" or "incomplete")
**Error Responses**:
- Invalid ID: "Error: Task with ID {id} not found"

### 6. Exit Flow
**Response**: Application terminates cleanly with no output

## Input Validation

### Menu Selection
- **Valid Input**: Numeric input between 1-6
- **Invalid Input Response**: "Invalid selection. Please enter a number between 1-6."
- **Non-numeric Input Response**: "Invalid input. Please enter a number between 1-6."

### Task ID Validation
- **Valid Input**: Positive integer corresponding to existing task
- **Invalid Input Response**: "Error: Task with ID {id} not found"
- **Non-numeric Input Response**: "Invalid input. Please enter a valid task ID."

### Title Validation
- **Valid Input**: Non-empty string
- **Invalid Input Response**: "Error: Title is required and cannot be empty"

## Common Error Responses
- **Invalid menu selection**: "Invalid selection. Please enter a number between 1-6."
- **Non-numeric input**: "Invalid input. Please enter a valid number."
- **General error**: "An error occurred: {error_message}"
- **Return to menu**: After each operation (success or failure), return to main menu unless exiting