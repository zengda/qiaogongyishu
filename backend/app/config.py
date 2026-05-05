import os
from dotenv import load_dotenv

_env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(_env_file)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
        'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'qiaogongyishu.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    PRODUCTION_DOMAIN = os.getenv('PRODUCTION_DOMAIN', 'qgys.rongyun.online')
    
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'local')
    LOCAL_UPLOAD_PATH = os.getenv('LOCAL_UPLOAD_PATH', '/uploads')
    LOCAL_BASE_URL = os.getenv('LOCAL_BASE_URL', 'http://localhost:5001/uploads')
    
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', '')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', '')
    OSS_REGION = os.getenv('OSS_REGION', '')
    
    MAX_FILE_SIZE = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    
    RATE_LIMIT_WINDOW = 60
    RATE_LIMIT_MAX = 1

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}