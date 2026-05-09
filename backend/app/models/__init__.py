from app.models.category import Category
from app.models.tag import Tag
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_tag import ProductTag
from app.models.banner import Banner
from app.models.customer import Customer
from app.models.admin import Admin
from app.models.system_setting import SystemSetting
from app.models.storage_config import StorageConfig

def init_data():
    """初始化预置数据"""
    from app.extensions import db
    
    if not Category.query.first():
        categories = [
            Category(name='一层', sort_order=1),
            Category(name='二层', sort_order=2),
            Category(name='三层', sort_order=3),
            Category(name='多层', sort_order=4),
            Category(name='双拼', sort_order=5)
        ]
        db.session.add_all(categories)
    
    if not Tag.query.first():
        tags = [
            Tag(name='新中式', sort_order=1),
            Tag(name='欧式', sort_order=2),
            Tag(name='现代', sort_order=3),
            Tag(name='中式', sort_order=4)
        ]
        db.session.add_all(tags)
    
    if not Admin.query.first():
        from werkzeug.security import generate_password_hash
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            real_name='管理员',
            role='super'
        )
        db.session.add(admin)
    
    if not StorageConfig.query.first():
        from app.config import Config as EnvConfig
        storage_config = StorageConfig(
            storage_type=EnvConfig.STORAGE_TYPE,
            local_upload_path=EnvConfig.LOCAL_UPLOAD_PATH,
            local_base_url=EnvConfig.LOCAL_BASE_URL,
            is_active=True
        )
        if EnvConfig.STORAGE_TYPE == 'oss':
            storage_config.oss_access_key_id = EnvConfig.OSS_ACCESS_KEY_ID
            storage_config.oss_access_key_secret = EnvConfig.OSS_ACCESS_KEY_SECRET
            storage_config.oss_bucket_name = EnvConfig.OSS_BUCKET_NAME
            storage_config.oss_endpoint = EnvConfig.OSS_ENDPOINT
        db.session.add(storage_config)
    
    db.session.commit()