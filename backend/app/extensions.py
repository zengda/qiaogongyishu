from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

db = SQLAlchemy()
migrate = Migrate()
redis_client = None

def init_extensions(app):
    """初始化Flask扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    global redis_client
    redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        decode_responses=True
    )