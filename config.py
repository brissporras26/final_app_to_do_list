#configuracion  URL de la base de datos y la clave secreta
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')  # URI de MongoDB desde las variables de entorno
    UPLOAD_FOLDER = 'app/static/uploads'
    #MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
