from flask import Blueprint, render_template, session, redirect, url_for
from database.database_manager import database_manager

home_bp = Blueprint('home', __name__)
#BRI
@home_bp.route('/home')
def home():
    # Verifica si el usuario está autenticado
    if not session.get('user_email') and not session.get('user'):
        return redirect(url_for('user.get_user'))

    # Obtén la colección de tareas de la base de datos
    tasks_collection = database_manager.get_db()['tasks']

    # Obtén el correo electrónico del usuario desde la sesión (login tradicional o OAuth)
    user_email = session.get('user_email') or session.get('user', {}).get('email')

    # Consulta las tareas asociadas al correo electrónico del usuario
    tasks = list(tasks_collection.find({'user_email': user_email}))

    # Asegúrate de convertir el campo '_id' a string para evitar problemas con Jinja2
    for task in tasks:
        task['_id'] = str(task['_id'])

    # Imprime las tareas para depuración
    print(f'Tasks to render: {tasks}')

    # Renderiza la plantilla con las tareas y el correo del usuario
    return render_template('home.html', tasks=tasks, user_email=user_email)
