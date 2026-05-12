from app.models.storage_config import StorageConfig
from app.services.storage.local import LocalStorage
from app.services.storage.oss import OSSStorage

_storage_backend = None

def get_storage_backend():
    """获取存储服务实例（单例模式）"""
    global _storage_backend
    if _storage_backend is None:
        config = StorageConfig.query.filter_by(is_active=True).first()
        if not config:
            raise Exception("未配置存储服务")
        
        if config.storage_type == 'oss':
            _storage_backend = OSSStorage(
                config.oss_access_key_id,
                config.oss_access_key_secret,
                config.oss_bucket_name,
                config.oss_endpoint,
                config.oss_cdn_domain,
                config.oss_custom_domain,
                config.oss_bucket_domain,
                config.oss_https_enabled
            )
        else:
            _storage_backend = LocalStorage(
                config.local_upload_path or '/uploads',
                config.local_base_url or 'http://localhost:5001/uploads'
            )
    return _storage_backend

def reset_storage_backend():
    """重置存储服务实例（用于配置变更后）"""
    global _storage_backend
    _storage_backend = None