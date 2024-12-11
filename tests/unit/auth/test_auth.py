import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app.logic.task_logic import add_task_logic, get_task_by_name, update_task

@pytest.fixture
def mock_user():
    return {
        '_id': ObjectId(),
        'email': 'test@example.com',
        'tasks': []
    }

@pytest.fixture
def mock_task():
    return {
        '_id': ObjectId(),
        'name': 'Test Task',
        'priority': 'high',
        'user_id': ObjectId()
    }

@patch('app.logic.task_logic.database_manager')
def test_add_task_logic_success(mock_db, mock_user):
    # Setup mock database responses
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([mock_user])
    mock_db.select.return_value = mock_cursor
    
    # Mock the insert operation
    task_id = ObjectId()
    mock_db.insert.return_value = task_id
    
    # Call the function
    result = add_task_logic(mock_user['email'], 'New Task', 'high')
    
    # Verify the results
    assert result == task_id
    mock_db.insert.assert_called_once()
    mock_db.update.assert_called_once()

@patch('app.logic.task_logic.database_manager')
def test_add_task_logic_user_not_found(mock_db):
    # Setup mock to return empty result
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([])
    mock_db.select.return_value = mock_cursor
    
    # Verify that ValueError is raised
    with pytest.raises(ValueError, match="Usuario no encontrado."):
        add_task_logic('nonexistent@example.com', 'Task Name', 'high')

@patch('app.logic.task_logic.database_manager')
def test_get_task_by_name_success(mock_db, mock_user, mock_task):
    # Setup mock database responses
    mock_user_cursor = MagicMock()
    mock_user_cursor.__iter__.return_value = iter([mock_user])
    mock_task_cursor = MagicMock()
    mock_task_cursor.__iter__.return_value = iter([mock_task])
    
    mock_db.select.side_effect = [mock_user_cursor, mock_task_cursor]
    
    # Call the function
    result = get_task_by_name(mock_user['email'], mock_task['name'])
    
    # Verify the results
    assert result == mock_task
    assert mock_db.select.call_count == 2

@patch('app.logic.task_logic.database_manager')
def test_get_task_by_name_task_not_found(mock_db, mock_user):
    # Setup mock responses
    mock_user_cursor = MagicMock()
    mock_user_cursor.__iter__.return_value = iter([mock_user])
    mock_task_cursor = MagicMock()
    mock_task_cursor.__iter__.return_value = iter([])
    
    mock_db.select.side_effect = [mock_user_cursor, mock_task_cursor]
    
    # Call the function
    result = get_task_by_name(mock_user['email'], 'Nonexistent Task')
    
    # Verify result is None
    assert result is None

@patch('app.logic.task_logic.database_manager')
def test_update_task_success(mock_db, mock_task):
    # Setup mock database response
    mock_db.update.return_value = 1
    
    # Call the function
    result = update_task(str(mock_task['_id']), 'Updated Task', 'medium')
    
    # Verify the results
    assert result is True
    mock_db.update.assert_called_once()

@patch('app.logic.task_logic.database_manager')
def test_update_task_failure(mock_db, mock_task):
    # Setup mock to return 0 updated documents
    mock_db.update.return_value = 0
    
    # Call the function
    result = update_task(str(mock_task['_id']), 'Updated Task', 'medium')
    
    # Verify the results
    assert result is False