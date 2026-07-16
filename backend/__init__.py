import os
from flask import Flask, url_for # type: ignore
from flask_login import LoginManager # type: ignore
from dotenv import load_dotenv
import flask_sqlalchemy #type: ignore

db = flask_sqlalchemy.SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "url_for('/')"

def create_app():
    load_dotenv()
    

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    
    app = Flask(__name__, template_folder=template_dir)

    app.config['SECRET_KEY'] = os.getenv('KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from . import models

    from .routes_pages import pages_bp
    app.register_blueprint(pages_bp)

    login_manager.init_app(app)


    from .models import user

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))

    return app