from flask import Blueprint, request, jsonify, url_for, render_template, session, flash, redirect
from database.database_manager import database_manager
from bson import ObjectId
import os
from app.logic.task_logic import add_task_logic, update_task

task_bp = Blueprint('task', __name__)

# Accede a las variables de entorno
DB_URI = os.getenv('MONGO_URI')

@task_bp.route('/tasks', methods=['GET'])
def list_tasks():
    # Obtener la colección de tareas directamente desde la instancia de database_manager
    tasks_collection = database_manager.get_db()['tasks']
    tasks = list(tasks_collection.find())  # Obtener todas las tareas y convertir el cursor a una lista
    return jsonify(tasks)

@task_bp.route('/add-task', methods=['POST'])
def add_task():
    # Verifica si el usuario está autenticado
    if 'user_email' not in session:
        flash("Debes iniciar sesión para agregar una tarea.", 'error')
        return redirect(url_for('user.get_user'))  # Redirige al login si no está autenticado
    
    task_name = request.form.get('task_name')
    task_priority = request.form.get('task_priority')

    try:
        # Obtén el email del usuario desde la sesión
        user_email = session['user_email']
        
        # Llama a la lógica para agregar la tarea
        add_task_logic(user_email, task_name, task_priority)
        flash("Tarea agregada exitosamente.", 'success')
        return redirect(url_for('home.home'))  # Redirige de vuelta a la página de inicio
    except ValueError as e:
        flash(str(e), 'error')  # Muestra el error si el usuario no está encontrado
        return redirect(url_for('home.home'))

@task_bp.route('/edit-task/<task_id>', methods=['POST'])
def edit_task(task_id):
    # Verifica si el usuario está autenticado
    if 'user_email' not in session:
        flash("Debes iniciar sesión para editar una tarea.", 'error')
        return redirect(url_for('user.get_user'))  # Redirige al login si no está autenticado

    new_name = request.form.get('new_name')
    new_priority = request.form.get('new_priority')

    print("[NAVA] task_id " + task_id)
    print("[NAVA] new_name " + new_name)
    print("[NAVA] new_priority " + new_priority)

    try:
        update_task(task_id, new_name, new_priority)
        flash("Tarea actualizada exitosamente.", 'success')
    except Exception as e:
        flash(f"Error al actualizar la tarea: {e}", 'error')
    return redirect(url_for('home.home'))

@task_bp.route('/tasks-delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    # Verifica si el usuario está autenticado
    if 'user_email' not in session:
        flash("Debes iniciar sesión para eliminar una tarea.", 'error')
        return redirect(url_for('user.get_user'))  # Redirige al login si no está autenticado
    
    if request.form.get('_method') == 'DELETE':
        print(f"Request method: {request.method}")  
        print(f"Task ID received: {task_id}")  

        try:
            # Convertir task_id a ObjectId
            query = {'_id': ObjectId(task_id)}

            deleted_count = database_manager.delete('tasks', query)

            if deleted_count > 0:
                print(f"Tarea con ID {task_id} eliminada correctamente.")
                flash(f"Tarea con ID {task_id} eliminada correctamente.", 'success')
                return redirect(url_for('home.home'))
            else:
                print(f"No se encontró una tarea con ID {task_id}.")
                flash(f"No se encontró una tarea con ID {task_id}.", 'error')
                return redirect(url_for('home.home'))
        except Exception as e:
            print(f"Error al eliminar la tarea: {e}")
            flash(f"Error al eliminar la tarea: {e}", 'error')
            return redirect(url_for('home.home'))
    else:
        return redirect(url_for('home.home'))