from flask import Blueprint, redirect, url_for, session, request, flash, render_template
from app.logic.users_logic import register_user_logic, login_user_logic, auth_callback_logic, logout_user_logic
from app import oauth  # Add this import

import os

# Blueprint para las rutas de usuario
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def add_user():
    """
    Ruta para registrar un nuevo usuario.
    """
    if request.method == 'POST':
        email_user = request.form.get('email')
        password_user = request.form.get('password')

        # Llamar a la lógica para registrar el usuario
        register_user_logic(email_user, password_user)
        flash("Registro exitoso. Por favor inicia sesión.", 'success')
        return redirect(url_for('user.get_user'))

    return render_template('register.html')

@user_bp.route('/', methods=['GET', 'POST'])
def get_user():
    """
    Ruta para manejar el inicio de sesión local.
    """
    # If user is already authenticated, redirect to home
    if session.get('authenticated'):
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Llamar a la lógica para verificar el inicio de sesión
        if login_user_logic(email, password):
            flash("Has iniciado sesión exitosamente.", 'success')
            session['user_email'] = email
            session['authenticated'] = True  # Add this line
            return redirect(url_for('home.home'))
        else:
            flash("Email o contraseña incorrectos.", 'error')

    return render_template('login.html')

    return render_template('login.html')

@user_bp.route('/login')
def login():
    """
    Redirige al usuario a Auth0 para autenticación.
    """
    # Ensure we have the full URL for the callback
    callback_url = url_for('user.auth_callback', _external=True)
    print(f"Callback URL: {callback_url}")  # Debug print
    
    try:
        return oauth.auth0.authorize_redirect(
            redirect_uri=callback_url,
            audience=f"https://{os.getenv('AUTH0_DOMAIN')}/userinfo",
            prompt='login'  # Force login prompt
        )
    except Exception as e:
        print(f"Error in login route: {str(e)}")  # Debug print
        flash(f"Error al iniciar sesión con Auth0: {str(e)}", "error")
        return redirect(url_for('user.get_user'))

@user_bp.route('/auth/callback')
def auth_callback():
    """
    Maneja el callback después de la autenticación en Auth0.
    """
    try:
        # Get the token from Auth0
        token = oauth.auth0.authorize_access_token()
        
        # Get the user info from Auth0 - Fix the URL
        userinfo_url = f"https://{os.getenv('AUTH0_DOMAIN')}/userinfo"
        resp = oauth.auth0.get(userinfo_url)
        userinfo = resp.json()
        
        print(f"Auth0 user info: {userinfo}")  # Debug print
        
        # Store user info in session
        session['user_email'] = userinfo['email']
        session['user'] = userinfo
        session['authenticated'] = True
        
        # Register user if they don't exist
        register_user_logic(userinfo['email'])
        
        # Redirect to home after successful login
        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for('home.home'))
        
    except Exception as e:
        print(f"Auth callback error: {str(e)}")  # Debug print
        flash(f"Error en la autenticación: {str(e)}", "error")
        return redirect(url_for('user.get_user'))

@user_bp.route('/logout')
def logout():
    """
    Cierra la sesión del usuario y redirige a la página principal.
    """
    result = logout_user_logic(session)
    flash(result['message'], result['status'])
    return redirect(result['redirect_url'])