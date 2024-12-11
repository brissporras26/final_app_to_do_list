import pytest
from app.logic.users_logic import register_user_logic, login_user_logic
from database.database_manager import database_manager
from werkzeug.security import check_password_hash

@pytest.fixture
def user_fixture():
    email = "testuser@example.com"
    password = "password123"
    # Llamamos al método de registro
    register_user_logic(email, password)
    return email, password

def test_register_user(user_fixture):
    email, password = user_fixture
    # Verificamos si el usuario fue registrado correctamente en la base de datos
    user = database_manager.select(
        db_name=None,
        collection_name="users",
        query={"email": email}
    )
    user_list = list(user)
    assert user_list is not None
    assert user_list[0]['email'] == email
    assert check_password_hash(user_list[0]['password'], password)

def test_register_user_without_password():
    # Prueba de registro sin contraseña
    email = "user_no_password@example.com"
    register_user_logic(email)  # No pasamos contraseña
    user = database_manager.select(
        db_name=None,
        collection_name="users",
        query={"email": email}
    )
    user_list = list(user)
    assert user_list is not None
    assert user_list[0]['email'] == email
    assert user_list[0]['password'] is None  # La contraseña debe ser None si no se pasa