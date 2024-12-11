<!-- testing.md -->
# Testing Guide

## Test Structure

The test suite is organized into several key files:

- `conftest.py`: Global test fixtures and configurations
- `test_system.py`: System-level integration tests
- `test_user_logic.py`: User management logic tests
- `test_login_logic.py`: Authentication logic tests
- `test_task.py`: Task management logic tests

## Running Tests

### Basic Test Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_system.py

# Run tests with coverage
pytest --cov=app tests/

# Run tests with verbose output
pytest -v
```

## Test Fixtures

### Global Fixtures

```python
# conftest.py
@pytest.fixture(scope="module")
def app():
    """Create application for testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'MONGO_URI': 'mongodb://localhost:27017/test_db',
        'WTF_CSRF_ENABLED': False
    })
    return app
```

### Authentication Fixtures

```python
@pytest.fixture(scope="function")
def test_user():
    """Test user fixture"""
    return {
        'email': 'test@example.com',
        'password': 'test_password'
    }
```

## Test Categories

### User Authentication Tests
- Registration flow
- Login validation
- Session management
- Unauthorized access handling

### Task Management Tests
- Task creation
- Task listing
- Task editing
- Task deletion

### Integration Tests
- Full user workflows
- Session handling
- Database operations

---