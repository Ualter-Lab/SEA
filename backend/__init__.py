import os
from flask import Flask

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    
    app = Flask(__name__, template_folder=template_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sea1112@localhost:5432/Sea'
    
    from .routes_pages import pages_bp
    app.register_blueprint(pages_bp)

    return app