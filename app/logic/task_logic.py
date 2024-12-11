import uuid
from database.database_manager import database_manager
from bson import ObjectId

def add_task_logic(user_email, task_name, task_priority):
    """
    Lógica para agregar una tarea asociada a un usuario.
    """
    # Buscar al usuario por su email
    user = database_manager.select(
        db_name=None,
        collection_name='users',
        query={'email': user_email}
    )
    user_list = list(user)

    if not user_list:
        raise ValueError("Usuario no encontrado.")

    user_id = user_list[0]['_id']

    # Crear un diccionario con los datos de la tarea, incluyendo el user_email
    task_data = {
        'name': task_name,
        'priority': task_priority,
        'user_email': user_email,  # Agrega el campo user_email aquí
        'user_id': ObjectId(user_id)  # Asociamos la tarea al usuario
    }

    # Insertar la tarea en la base de datos
    inserted_id = database_manager.insert(
        db_name=None,
        collection_name='tasks',
        data=task_data
    )

    # Actualizamos la lista de tareas del usuario
    user_tasks = user_list[0].get('tasks', [])
    user_tasks.append(ObjectId(inserted_id))

    # Actualizar el usuario con la nueva tarea
    database_manager.update(
        db_name=None,
        collection_name='users',
        query={'_id': ObjectId(user_id)},
        update_data={'tasks': user_tasks}
    )

    return inserted_id



def get_task_by_name(user_email, task_name):
    """
    Busca una tarea en la colección 'tasks' por su nombre y asociada a un usuario.
    :param user_email: Email del usuario.
    :param task_name: Nombre de la tarea.
    :return: Documento de la tarea si se encuentra, None en caso contrario.
    """
    try:
        # Buscar al usuario por su email
        user = database_manager.select(
            db_name=None,
            collection_name='users',
            query={'email': user_email}
        )
        user_list = list(user)

        if not user_list:
            raise ValueError("Usuario no encontrado.")

        user_id = user_list[0]['_id']

        # Buscar la tarea por nombre y user_id
        task = database_manager.select(
            db_name=None,
            collection_name='tasks',
            query={'name': task_name, 'user_id': ObjectId(user_id)}
        )
        task_list = list(task)

        if not task_list:
            return None
        return task_list[0]
    except Exception as e:
        print(f"Error al obtener la tarea: {e}")
        raise


def update_task(task_id, new_name=None, new_priority=None):
    """
    Actualiza una tarea en la colección 'tasks'.
    :param task_id: ID de la tarea a actualizar.
    :param new_name: Nuevo nombre de la tarea (opcional).
    :param new_priority: Nueva prioridad de la tarea (opcional).
    :return: True si la actualización fue exitosa, False en caso contrario.
    """
    try:
        update_data = {}
        if new_name:
            update_data['name'] = new_name
        if new_priority:
            update_data['priority'] = new_priority

        if not update_data:
            return False  # No hay nada que actualizar

        update_result = database_manager.update(
            db_name=None, 
            collection_name='tasks', 
            query={'_id': ObjectId(task_id)}, 
            update_data=update_data
        )
        return update_result > 0
    except Exception as e:
        print(f"Error al actualizar la tarea: {e}")
        raise