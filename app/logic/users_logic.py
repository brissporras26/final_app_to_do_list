from database.database_manager import database_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, session, redirect
import os
from app import oauth  # Asegúrate de importar oauth desde la configuración de app

def register_user_logic(email_user, password_user=None):
    """
    Lógica para registrar un nuevo usuario.
    """
    # Check if user already exists
    existing_user = database_manager.select(
        db_name=None,
        collection_name='users',
        query={'email': email_user}
    )
    
    if list(existing_user):
        return  # User already exists, no need to register again
        
    if password_user:
        hashed_password = generate_password_hash(password_user)
    else:
        hashed_password = None

    user_data = {
        'email': email_user,
        'password': hashed_password,
        'tasks': []
    }

    database_manager.insert(
        db_name=None,
        collection_name='users',
        data=user_data
    )

def login_user_logic(email_user, password_user):
    """
    Lógica para verificar las credenciales del usuario.
    """
    # Buscar al usuario por su email
    user = database_manager.select(
        db_name=None,
        collection_name='users',
        query={'email': email_user}
    )
    user_list = list(user)

    if not user_list:
        # Si no se encuentra el usuario en la base de datos
        return False

    # Obtener el hash de la contraseña almacenada
    stored_password_hash = user_list[0]['password']

    # Si no hay contraseña, retorna False
    if stored_password_hash is None:
        return False

    # Verificar si la contraseña está correctamente hasheada y coincide con la ingresada
    return check_password_hash(stored_password_hash, password_user)

def auth_callback_logic(session):
    """
    Lógica para manejar el callback de autenticación de Auth0.
    """
    try:
        # Verificar si el usuario ya está autenticado
        if 'user' in session:
            return {'message': 'Ya estás autenticado.', 'status': 'success', 'redirect_url': url_for('home.home')}

        # Obtener el token de Auth0
        token = oauth.authorize_access_token()
        if not token:
            return {'message': 'No se pudo obtener el token de Auth0.', 'status': 'error', 'redirect_url': url_for('user.auth_callback')}

        # Obtener la información del usuario
        user_info = oauth.parse_id_token(token)
        if not user_info:
            return {'message': 'Error al procesar el token del usuario.', 'status': 'error', 'redirect_url': url_for('user.auth_callback')}

        # Buscar al usuario por su correo electrónico en la base de datos
        user = database_manager.select(
            db_name=None,
            collection_name='users',
            query={'email': user_info['email']}
        )
        user_list = list(user)

        if not user_list:
            # Si el usuario no existe en la base de datos, registrarlo
            register_user_logic(user_info['email'])

        # Guardar la información del usuario en la sesión
        session['user'] = user_info
        return {'message': 'Inicio de sesión exitoso.', 'status': 'success', 'redirect_url': url_for('home.home')}

    except Exception as e:
        return {'message': f'Error: {str(e)}', 'status': 'error', 'redirect_url': url_for('user.auth_callback')}

def logout_user_logic(session):
    """
    Lógica para cerrar sesión del usuario.
    """
    # Eliminar solo la información relevante de la sesión
    session.clear()  # Limpiar toda la sesión

    return {
        'message': 'Has cerrado sesión.',
        'status': 'success',
        'redirect_url': f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?client_id={os.getenv("AUTH0_CLIENT_ID")}&returnTo={url_for("home.home", _external=True)}'
    }