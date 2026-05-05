import os
from flask import Flask
from flask import Flask
import flask_sqlalchemy #type: ignore

db = flask_sqlalchemy.SQLAlchemy()

def create_app():

    # Configurações do Flask
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    
    app = Flask(__name__, template_folder=template_dir)


    #Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sea.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from . import models

    # Rotas
    from .routes_pages import pages_bp
    app.register_blueprint(pages_bp)

    return app