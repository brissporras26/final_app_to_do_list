import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app.logic.task_logic import add_task_logic, get_task_by_name, update_task


@pytest.fixture
def mock_user_data():
    return {
        "_id": ObjectId(),
        "email": "testuser@example.com",
        "tasks": []
    }

@pytest.fixture
def mock_task_data():
    return {
        "_id": ObjectId(),
        "name": "Test Task",
        "priority": "High",
        "user_email": "testuser@example.com",
        "user_id": ObjectId()
    }

# Test for adding a task
@patch('app.logic.task_logic.database_manager')
def test_add_task_logic(mock_db, mock_user_data):
    # Mock user query result
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([mock_user_data])
    mock_db.select.return_value = mock_cursor

    # Mock insert operation
    mock_db.insert.return_value = ObjectId()

    # Mock update operation
    mock_db.update.return_value = 1

    # Call the function
    result = add_task_logic(mock_user_data["email"], "Test Task", "High")

    # Assertions
    assert result is not None
    mock_db.select.assert_called_once_with(db_name=None, collection_name='users', query={'email': mock_user_data["email"]})
    mock_db.insert.assert_called_once()
    mock_db.update.assert_called_once()

# Test for getting a task by name
@patch('app.logic.task_logic.database_manager')
def test_get_task_by_name(mock_db, mock_user_data, mock_task_data):
    # Mock user query result
    mock_user_cursor = MagicMock()
    mock_user_cursor.__iter__.return_value = iter([mock_user_data])
    mock_db.select.side_effect = [mock_user_cursor, [mock_task_data]]

    # Call the function
    result = get_task_by_name(mock_user_data["email"], "Test Task")

    # Assertions
    assert result == mock_task_data
    mock_db.select.assert_any_call(db_name=None, collection_name='users', query={'email': mock_user_data["email"]})
    mock_db.select.assert_any_call(db_name=None, collection_name='tasks', query={'name': "Test Task", 'user_id': mock_user_data["_id"]})

# Test for updating a task
@patch('app.logic.task_logic.database_manager')
def test_update_task(mock_db, mock_task_data):
    # Mock update operation
    mock_db.update.return_value = 1

    # Call the function
    result = update_task(mock_task_data["_id"], new_name="Updated Task", new_priority="Medium")

    # Assertions
    assert result is True
    mock_db.update.assert_called_once_with(
        db_name=None,
        collection_name='tasks',
        query={'_id': mock_task_data["_id"]},
        update_data={'name': "Updated Task", 'priority': "Medium"}
    )

# Test for update task with no changes
@patch('app.logic.task_logic.database_manager')
def test_update_task_no_changes(mock_db):
    # Call the function without changes
    result = update_task(ObjectId())

    # Assertions
    assert result is False
    mock_db.update.assert_not_called()
