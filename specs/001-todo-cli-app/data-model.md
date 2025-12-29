# Data Model: In-Memory Python Todo CLI App

## Task Entity

The Task entity represents a single todo item with the following attributes:

### Attributes
- **id** (int): Unique identifier for each task, auto-generated as incrementing integer
- **title** (str): Required string representing the task name (non-empty)
- **description** (str): Optional string providing more details about the task (can be empty/null equivalent)
- **completed** (bool): Boolean indicating whether the task is complete (true) or incomplete (false), defaults to False

### Validation Rules
- Title must be provided and non-empty when creating a task
- ID must be unique within the application session
- ID must be a positive integer

### State Transitions
- **Creation**: New task is created with completed=False by default
- **Completion**: Task status changes from incomplete (False) to complete (True) when marked as complete
- **Reversion**: Task status changes from complete (True) back to incomplete (False) when marked as incomplete

## TaskCollection Entity

A container for managing multiple Task entities:

### Attributes
- **tasks** (dict): Dictionary mapping task IDs to Task objects for O(1) lookup
- **next_id** (int): Counter for generating unique IDs, starts at 1 and increments

### Operations
- **add_task(title, description)**: Creates new Task with unique ID and adds to collection
- **get_task(task_id)**: Retrieves a task by its ID
- **update_task(task_id, title=None, description=None)**: Updates specified task attributes
- **delete_task(task_id)**: Removes task from collection
- **get_all_tasks()**: Returns all tasks in the collection
- **toggle_completion(task_id)**: Toggles the completion status of a task