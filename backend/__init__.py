import os
from flask import Flask, render_template # type: ignore
from flask_login import LoginManager # type: ignore
from dotenv import load_dotenv
import flask_sqlalchemy #type: ignore
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = flask_sqlalchemy.SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "pages.login"

def create_app():
    load_dotenv()

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

    
    app = Flask(__name__, template_folder=template_dir)


    @app.errorhandler(404)
    def pagina_nao_encontrada(error):
        return render_template("page404.html"), 404

    secret_key = os.getenv('KEY')
    database_url = os.getenv('DATABASE_URL')

    if not secret_key or not database_url:
        raise ValueError("KEY e DATABASE_URL devem estar definidas no arquivo .env")

    limiter = Limiter(key_func=get_remote_address)

    app.config['SECRET_KEY'] = os.getenv('KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    files_path = os.getenv("FILES_PATH")
    if not files_path:
        raise RuntimeError("FILES_PATH não definido no .env")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True   
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024 
        

    from . import models

    from .routes_pages import pages_bp
    app.register_blueprint(pages_bp)

    db.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)


    from .models import user

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))

    return app