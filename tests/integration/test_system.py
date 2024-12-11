import pytest
from flask import session, json
from werkzeug.security import generate_password_hash
from bson import ObjectId

@pytest.fixture(scope="function")
def test_user():
    """Test user fixture"""
    return {
        'email': 'test@example.com',
        'password': 'test_password'
    }

@pytest.fixture(scope="function")
def authenticated_client(client, test_user):
    """Create an authenticated client session"""
    # Register user
    client.post('/register', data=test_user, follow_redirects=True)
    
    # Log in user
    with client.session_transaction() as sess:
        sess['user_email'] = test_user['email']
        sess['authenticated'] = True
    return client

# Test Database Connection
@pytest.fixture(scope="function")
def mock_db():
    """Mock database for testing"""
    class MockDB:
        def __init__(self):
            self.users = {}
            self.tasks = {}
            self._db = {
                'users': {},
                'tasks': {}
            }

        def get_db(self):
            return self._db

        def insert(self, collection_name, data):
            collection = self._db.get(collection_name, {})
            _id = ObjectId()
            data['_id'] = _id
            collection[str(_id)] = data
            return _id

        def select(self, collection_name, query):
            collection = self._db.get(collection_name, {})
            results = []
            for item in collection.values():
                matches = all(
                    str(item.get(k)) == str(v) if isinstance(v, ObjectId) else item.get(k) == v
                    for k, v in query.items()
                )
                if matches:
                    results.append(item)
            return results

        def update(self, collection_name, query, update_data):
            collection = self._db.get(collection_name, {})
            updated = 0
            for item in collection.values():
                if all(str(item.get(k)) == str(v) if isinstance(v, ObjectId) else item.get(k) == v
                      for k, v in query.items()):
                    item.update(update_data)
                    updated += 1
            return updated

        def delete(self, collection_name, query):
            collection = self._db.get(collection_name, {})
            initial_size = len(collection)
            items_to_delete = []
            for _id, item in collection.items():
                if all(str(item.get(k)) == str(v) if isinstance(v, ObjectId) else item.get(k) == v
                      for k, v in query.items()):
                    items_to_delete.append(_id)
            for _id in items_to_delete:
                del collection[_id]
            return initial_size - len(collection)

    mock_db_instance = MockDB()
    import database.database_manager
    database.database_manager.database_manager = mock_db_instance
    return mock_db_instance

def test_user_registration_and_login_flow(client, mock_db, test_user):
    """Test user registration and login process"""
    # Test registration
    response = client.post('/register', data=test_user, follow_redirects=True)
    assert response.status_code == 200

    # Test login page access
    response = client.get('/')
    assert response.status_code == 200

    # Test login
    response = client.post('/', data=test_user, follow_redirects=True)
    assert response.status_code == 200

def test_add_task(authenticated_client, mock_db):
    """Test adding a new task"""
    response = authenticated_client.post('/add-task', data={
        'task_name': 'Test Task',
        'task_priority': 'high'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_list_tasks(authenticated_client, mock_db):
    """Test listing tasks"""
    # Add a test task first
    authenticated_client.post('/add-task', data={
        'task_name': 'Test List Task',
        'task_priority': 'high'
    })

    # Get tasks
    response = authenticated_client.get('/home')
    assert response.status_code == 200

def test_edit_task(authenticated_client, mock_db):
    """Test editing a task"""
    # Add a task first
    authenticated_client.post('/add-task', data={
        'task_name': 'Task to Edit',
        'task_priority': 'high'
    })
    
    tasks = mock_db.select('tasks', {'name': 'Task to Edit'})
    if tasks:
        task_id = str(tasks[0]['_id'])
        response = authenticated_client.post(f'/edit-task/{task_id}', data={
            'new_name': 'Edited Task',
            'new_priority': 'medium'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_task_operations_without_authentication(client):
    """Test task operations without authentication"""
    response = client.post('/add-task', data={
        'task_name': 'Unauthorized Task',
        'task_priority': 'low'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data

def test_home_page_access(client, authenticated_client):
    """Test home page access"""
    # Without authentication
    response = client.get('/home', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data

    # With authentication
    response = authenticated_client.get('/home')
    assert response.status_code == 200
    assert b'To-Do List' in response.data

def test_logout(authenticated_client):
    """Test logout functionality"""
    # Make sure we're authenticated first
    with authenticated_client.session_transaction() as sess:
        assert 'user_email' in sess
        assert sess.get('authenticated', False) is True

    # Call logout without following redirects
    response = authenticated_client.get('/logout', follow_redirects=False)
    
    # Check that we got a redirect status code
    assert response.status_code == 302
    
    # Verify that the session is cleared
    with authenticated_client.session_transaction() as sess:
        assert 'user_email' not in sess
        assert 'authenticated' not in sess
        
    # Verify that we can't access protected routes anymore
    home_response = authenticated_client.get('/home', follow_redirects=True)
    assert b'Login' in home_response.data or b'login' in home_response.data