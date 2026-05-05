from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
from flask import current_app

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

def get_redis_client():
    """获取Redis客户端连接"""
    global redis_client
    if redis_client is None:
        # 如果redis_client未初始化，尝试使用current_app配置初始化
        try:
            redis_client = redis.Redis(
                host=current_app.config['REDIS_HOST'],
                port=current_app.config['REDIS_PORT'],
                db=current_app.config['REDIS_DB'],
                decode_responses=True
            )
        except Exception:
            pass
    return redis_client