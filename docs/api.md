<!-- api.md -->
# API Documentation

## User Management API

### Register User

```python
def register_user_logic(email: str, password: str = None) -> bool:
    """
    Register a new user in the system.
    
    Args:
        email (str): User's email address
        password (str, optional): User's password. If None, creates passwordless user
        
    Returns:
        bool: True if registration successful, False otherwise
    """
```

### Login User

```python
def login_user_logic(email: str, password: str) -> bool:
    """
    Authenticate user credentials.
    
    Args:
        email (str): User's email address
        password (str): User's password
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
```

## Task Management API

### Add Task

```python
def add_task_logic(user_email: str, task_name: str, priority: str) -> ObjectId:
    """
    Add a new task for a user.
    
    Args:
        user_email (str): Email of the task owner
        task_name (str): Name of the task
        priority (str): Task priority level
        
    Returns:
        ObjectId: ID of the created task
        
    Raises:
        ValueError: If user not found
    """
```

### Update Task

```python
def update_task(task_id: str, new_name: str, new_priority: str) -> bool:
    """
    Update an existing task.
    
    Args:
        task_id (str): ID of the task to update
        new_name (str): New task name
        new_priority (str): New task priority
        
    Returns:
        bool: True if update successful, False otherwise
    """
```

---