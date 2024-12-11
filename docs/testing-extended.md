# Testing Documentation

## Overview

The Todo App uses pytest as its primary testing framework, with a comprehensive suite covering unit tests, integration tests, and end-to-end testing scenarios.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configurations
├── test_system.py          # System/Integration tests
├── test_user_logic.py      # User management unit tests
├── test_login_logic.py     # Authentication unit tests
└── test_task.py           # Task management unit tests
```

## Test Categories

### 1. Unit Tests

#### User Logic Tests
Tests for individual user management functions:

```python
# test_user_logic.py
def test_register_user(user_fixture):
    """Test user registration logic"""
    email, password = user_fixture
    user = database_manager.select(
        collection_name="users",
        query={"email": email}
    )
    user_list = list(user)
    assert user_list[0]['email'] == email
    assert check_password_hash(user_list[0]['password'], password)
```

#### Task Logic Tests
Tests for task management functions:

```python
# test_task.py
@patch('app.logic.task_logic.database_manager')
def test_add_task_logic_success(mock_db, mock_user):
    """Test successful task creation"""
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([mock_user])
    mock_db.select.return_value = mock_cursor
    
    task_id = ObjectId()
    mock_db.insert.return_value = task_id
    
    result = add_task_logic(mock_user['email'], 'New Task', 'high')
    assert result == task_id
```

### 2. Integration Tests

#### Authentication Flow
Tests for complete authentication workflows:

```python
def test_user_registration_and_login_flow(client, mock_db, test_user):
    """Test complete registration and login process"""
    # Test registration
    reg_response = client.post('/register', data=test_user)
    assert reg_response.status_code == 200
    
    # Test login
    login_response = client.post('/', data=test_user)
    assert login_response.status_code == 200
    
    # Test authenticated access
    home_response = client.get('/home')
    assert home_response.status_code == 200
    assert b'To-Do List' in home_response.data
```

#### Task Management Flow
Tests for task operations with authentication:

```python
def test_task_lifecycle(authenticated_client, mock_db):
    """Test complete task lifecycle"""
    # Create task
    create_response = authenticated_client.post('/add-task', data={
        'task_name': 'Lifecycle Task',
        'task_priority': 'high'
    })
    assert create_response.status_code == 200
    
    # Get task list
    list_response = authenticated_client.get('/home')
    assert b'Lifecycle Task' in list_response.data
    
    # Edit task
    tasks = mock_db.select('tasks', {'name': 'Lifecycle Task'})
    task_id = str(tasks[0]['_id'])
    edit_response = authenticated_client.post(f'/edit-task/{task_id}', data={
        'new_name': 'Updated Task',
        'new_priority': 'medium'
    })
    assert edit_response.status_code == 200
```

## Test Fixtures

### Global Fixtures

```python
# conftest.py
@pytest.fixture(scope="module")
def app():
    """Create test application instance"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'MONGO_URI': 'mongodb://localhost:27017/test_db',
        'WTF_CSRF_ENABLED': False
    })
    return app

@pytest.fixture(scope="module")
def client(app):
    """Create test client"""
    return app.test_client()
```

### Authentication Fixtures

```python
@pytest.fixture(scope="function")
def authenticated_client(client, test_user):
    """Create authenticated client session"""
    client.post('/register', data=test_user)
    with client.session_transaction() as sess:
        sess['user_email'] = test_user['email']
        sess['authenticated'] = True
    return client
```

### Database Fixtures

```python
@pytest.fixture(scope="function")
def mock_db():
    """Create mock database instance"""
    class MockDB:
        def __init__(self):
            self._db = {'users': {}, 'tasks': {}}
            
        def insert(self, collection_name, data):
            _id = ObjectId()
            data['_id'] = _id
            self._db[collection_name][str(_id)] = data
            return _id
            
        def select(self, collection_name, query):
            collection = self._db[collection_name]
            return [item for item in collection.values() 
                   if all(item.get(k) == v for k, v in query.items())]
    
    mock_db_instance = MockDB()
    return mock_db_instance
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_system.py

# Run tests matching pattern
pytest -k "test_user"

# Run with coverage report
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v
```

### Coverage Report

The coverage report helps identify untested code paths:

```bash
pytest --cov=app --cov-report=term-missing
```

Example output:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app/__init__.py            20      0   100%
app/routes.py             45      5    89%   45-48, 72
app/models.py             30      2    93%   102, 105
-----------------------------------------------------
TOTAL                     95      7    93%
```

## Best Practices

### 1. Test Organization

- Group related tests in the same file
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Keep tests focused and atomic

### 2. Mocking

```python
@patch('app.logic.task_logic.database_manager')
def test_with_mock(mock_db):
    # Configure mock
    mock_db.select.return_value = [{'_id': ObjectId(), 'name': 'Test'}]
    
    # Use mock in test
    result = your_function()
    
    # Verify mock interactions
    mock_db.select.assert_called_once()
```

### 3. Assertions

Use appropriate assertions:

```python
# Equality
assert result == expected_value

# Membership
assert item in collection

# Exception handling
with pytest.raises(ValueError):
    function_that_raises()

# Response status
assert response.status_code == 200

# Response content
assert b'Expected Content' in response.data
```

### 4. Test Data

```python
@pytest.fixture
def sample_task_data():
    """Provide consistent test data"""
    return {
        'task_name': 'Test Task',
        'task_priority': 'high',
        'user_id': ObjectId()
    }
```

## Troubleshooting Tests

### Common Issues

1. Database Connection Problems
```python
# Solution: Use mock_db fixture
@pytest.mark.usefixtures("mock_db")
def test_database_operation():
    # Test will use mock database
```

2. Authentication Issues
```python
# Solution: Use authenticated_client
def test_protected_route(authenticated_client):
    response = authenticated_client.get('/protected')
    assert response.status_code == 200
```

3. Session Management
```python
# Solution: Manually manage session
with client.session_transaction() as sess:
    sess['user_email'] = 'test@example.com'
    sess['authenticated'] = True
```

### Debugging Tips

1. Use pytest's `-v` flag for verbose output
2. Use `pytest.set_trace()` for debugging
3. Print debug information with `-s` flag
4. Use `--pdb` flag to drop into debugger on failures

## Continuous Integration

### GitHub Actions Configuration

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=app
```