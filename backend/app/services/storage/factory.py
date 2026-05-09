import os
from app.models.storage_config import StorageConfig
from app.services.storage.local import LocalStorage
from app.services.storage.oss import OSSStorage

_storage_backend = None

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _resolve_local_path(upload_path):
    if not upload_path:
        upload_path = 'uploads'
    if os.path.isabs(upload_path):
        return upload_path
    return os.path.join(_PROJECT_ROOT, upload_path)


def _db_or_env(db_val, env_val):
    return db_val if db_val else env_val


def get_storage_backend():
    """获取存储服务实例（单例模式），DB 配置优先，env 变量作为 fallback"""
    global _storage_backend
    if _storage_backend is not None:
        return _storage_backend

    from app.config import Config as EnvConfig

    config = StorageConfig.query.filter_by(is_active=True).first()

    storage_type = config.storage_type if config else EnvConfig.STORAGE_TYPE

    if storage_type == 'oss':
        _storage_backend = OSSStorage(
            access_key_id=_db_or_env(config.oss_access_key_id if config else '', EnvConfig.OSS_ACCESS_KEY_ID),
            access_key_secret=_db_or_env(config.oss_access_key_secret if config else '', EnvConfig.OSS_ACCESS_KEY_SECRET),
            bucket_name=_db_or_env(config.oss_bucket_name if config else '', EnvConfig.OSS_BUCKET_NAME),
            endpoint=_db_or_env(config.oss_endpoint if config else '', EnvConfig.OSS_ENDPOINT),
            cdn_domain=_db_or_env(config.oss_cdn_domain if config else '', ''),
            custom_domain=_db_or_env(config.oss_custom_domain if config else '', ''),
            bucket_domain=_db_or_env(config.oss_bucket_domain if config else '', ''),
            https_enabled=config.oss_https_enabled if config else False,
        )
    else:
        local_upload_path = _resolve_local_path(
            _db_or_env(config.local_upload_path if config else '', EnvConfig.LOCAL_UPLOAD_PATH)
        )
        local_base_url = _db_or_env(config.local_base_url if config else '', EnvConfig.LOCAL_BASE_URL)
        _storage_backend = LocalStorage(local_upload_path, local_base_url)

    return _storage_backend

def reset_storage_backend():
    """重置存储服务实例（用于配置变更后）"""
    global _storage_backend
    _storage_backend = None