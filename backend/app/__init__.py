from flask import Flask
from app.config import config
from app.extensions import init_extensions
from app.api import register_blueprints

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    init_extensions(app)
    register_blueprints(app)
    
    return app