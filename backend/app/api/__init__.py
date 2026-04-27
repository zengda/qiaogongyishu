from app.api.auth import auth_bp
from app.api.product import product_bp
from app.api.category import category_bp
from app.api.tag import tag_bp
from app.api.banner import banner_bp
from app.api.customer import customer_bp
from app.api.upload import upload_bp
from app.api.admin import admin_bp
from app.api.settings import settings_bp

def register_blueprints(app):
    """注册所有API蓝图"""
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(product_bp, url_prefix='/api/v1')
    app.register_blueprint(category_bp, url_prefix='/api/v1')
    app.register_blueprint(tag_bp, url_prefix='/api/v1')
    app.register_blueprint(banner_bp, url_prefix='/api/v1')
    app.register_blueprint(customer_bp, url_prefix='/api/v1')
    app.register_blueprint(upload_bp, url_prefix='/api/v1')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(settings_bp, url_prefix='/api/v1')