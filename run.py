#punto de entrada para ejecutar la app
from app import create_app
#from database.database_manager import db 
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.run()