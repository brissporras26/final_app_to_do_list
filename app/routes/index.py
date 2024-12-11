from flask import Blueprint, render_template, session, redirect, url_for

index_bp = Blueprint('index', __name__)

@index_bp.route('/index')
def index():
    if session.get('authenticated'):
        return redirect(url_for('home.home'))
    return render_template('index.html')
