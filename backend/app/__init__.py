from flask import Flask, send_from_directory
from app.config import config
from app.extensions import init_extensions
from app.api import register_blueprints
import os

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    init_extensions(app)
    register_blueprints(app)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(os.path.dirname(base_dir), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(upload_folder, filename)
    
    return app