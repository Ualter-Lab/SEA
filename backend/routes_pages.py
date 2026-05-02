from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)

from .auth import auth_bp
pages_bp.register_blueprint(auth_bp)


@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@pages_bp.route('/aluno')
def aluno():
    return render_template('aluno.html')