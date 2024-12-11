from flask import Blueprint

#Definir los Blueprints
home_bp = Blueprint('home', __name__)
auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
task_bp = Blueprint('task', __name__)
index_bp = Blueprint('index', __name__)


