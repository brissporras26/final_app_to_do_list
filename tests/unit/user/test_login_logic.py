import pytest
from app.logic.users_logic import login_user_logic
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_user_data():
    return {
        "email": "testuser@example.com",
        "password": "password123"
    }

# Test for valid credentials
@patch('app.logic.users_logic.database_manager')
def test_login_user_valid_credentials(mock_db, mock_user_data):
    # Create mock cursor response
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([{
        "email": mock_user_data["email"],
        "password": "hashed_password"
    }])
    
    # Setup the mock
    mock_db.select.return_value = mock_cursor
    
    # Mock the password check to return True
    with patch('app.logic.users_logic.check_password_hash', return_value=True):
        result = login_user_logic(mock_user_data["email"], mock_user_data["password"])
        assert result is True

# Test for invalid credentials
@patch('app.logic.users_logic.database_manager')
def test_login_user_invalid_credentials(mock_db):
    # Setup empty result from database
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([])
    mock_db.select.return_value = mock_cursor
    
    result = login_user_logic("invalid@example.com", "wrongpassword")
    assert result is False

# Test for user without password
@patch('app.logic.users_logic.database_manager')
def test_login_user_without_password(mock_db, mock_user_data):
    # Create mock cursor response with null password
    mock_cursor = MagicMock()
    mock_cursor.__iter__.return_value = iter([{
        "email": mock_user_data["email"],
        "password": None
    }])
    
    # Setup the mock
    mock_db.select.return_value = mock_cursor
    
    result = login_user_logic(mock_user_data["email"], mock_user_data["password"])
    assert result is False