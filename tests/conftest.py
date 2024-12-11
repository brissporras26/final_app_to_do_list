# tests/conftest.py
import pytest
from app import create_app
import json
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

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
    
    # Configure the JSON encoder
    app.json = json
    app.json.JSONEncoder = CustomJSONEncoder
    return app

@pytest.fixture(scope="module")
def client(app):
    """Create client for testing"""
    return app.test_client()

@pytest.fixture(scope="module")
def runner(app):
    """Create runner for testing"""
    return app.test_cli_runner()