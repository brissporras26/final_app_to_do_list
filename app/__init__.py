from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import os
from authlib.integrations.flask_client import OAuth  # Add this import

# Create OAuth object
oauth = OAuth()

def create_app():
    app = Flask(__name__)

    load_dotenv()
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Configure Auth0
    oauth.init_app(app)
    oauth.register(
        "auth0",
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
            "prompt": "login"
        },
        authorize_url=f'https://{os.getenv("AUTH0_DOMAIN")}/authorize',
        access_token_url=f'https://{os.getenv("AUTH0_DOMAIN")}/oauth/token',
        server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )
    
    @app.before_request
    def before_request():
        if request.method == 'POST' and '_method' in request.form:
            request.method = request.form['_method'].upper()
    
    # Importar y registrar rutas
    with app.app_context():
        from app.routes.home import home_bp
        from app.routes.user import user_bp
        from app.routes.tasks import task_bp
        from app.routes.index import index_bp
        
        app.register_blueprint(home_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(task_bp)
        app.register_blueprint(index_bp)

    return app