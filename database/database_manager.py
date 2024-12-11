import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from ssl import CERT_NONE
import certifi

# Cargar variables de entorno del archivo .env
load_dotenv()

class DatabaseManager:
    """
    Clase que gestiona operaciones en la base de datos MongoDB.
    """

    def __init__(self):
        """
        Constructor de la clase.
        """
        self.client = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        self.default_db_name = 'ToDo'  # Nombre de la base de datos predeterminada

    def get_db(self, db_name=None):
        """
        Configuración para devolver la instancia de la base de datos.
        :param db_name: Nombre de la base de datos (si es None, usa la predeterminada).
        """
        if db_name is None:
            db_name = self.default_db_name
        return self.client[db_name]

    def insert(self, db_name: str, collection_name: str, data: dict) -> str:
        """
        Método para realizar una operación de inserción en la base de datos.
        :param db_name: Nombre de la base de datos
        :param collection_name: Nombre de la colección en la que se realizará la inserción.
        :param data: Datos a insertar en la colección.
        :return: ID del documento insertado.
        """
        collection = self.get_db(db_name)[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def select(self, db_name: str, collection_name: str, query: dict, projection: dict = None):
        """
        Método para realizar una operación de selección en la base de datos.
        :param db_name: Nombre de la base de datos
        :param collection_name: Nombre de la colección en la que se realizará la selección.
        :param query: Condiciones para la selección.
        :param projection: Campos a seleccionar (por defecto, todos).
        :return: Documentos que coinciden con la consulta.
        """
        collection = self.get_db(db_name)[collection_name]
        return collection.find(query, projection)

    def update(self, db_name: str, collection_name: str, query: dict, update_data: dict) -> int:
        """
        Método para realizar una operación de actualización en la base de datos.
        :param db_name: Nombre de la base de datos
        :param collection_name: Nombre de la colección en la que se realizará la actualización.
        :param query: Condiciones para la actualización.
        :param update_data: Datos a actualizar en la colección.
        :return: Resultado de la operación de actualización.
        """
        collection = self.get_db(db_name)[collection_name]
        result = collection.update_one(query, {'$set': update_data})
        return result.modified_count

    def delete(self, collection_name: str, query: dict) -> int:
        """
        Método para realizar una operación de eliminación en la base de datos.
        :param collection_name: Nombre de la colección en la que se realizará la eliminación.
        :param query: Condiciones para la eliminación.
        :return: Número de documentos eliminados.
        """
        collection = self.get_db()[collection_name] 
        result = collection.delete_one(query)
        return result.deleted_count


# Crear una instancia global de DatabaseManager
database_manager = DatabaseManager()
