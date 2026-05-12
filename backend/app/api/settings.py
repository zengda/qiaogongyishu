from flask import Blueprint, request
from app.models.system_setting import SystemSetting
from app.models.storage_config import StorageConfig
from app.extensions import db
from app.utils.response import success, error

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings/<string:key>', methods=['GET'])
def get_setting(key):
    """获取系统设置"""
    setting = SystemSetting.query.filter_by(setting_key=key).first()
    if not setting:
        return error(404, '设置项不存在'), 404
    return success({'value': setting.setting_value})

@settings_bp.route('/storage/config', methods=['GET'])
def get_storage_config():
    """获取存储配置"""
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        return success({
            'storage_type': 'local',
            'oss_endpoint': '',
            'oss_access_key_id': '',
            'oss_access_key_secret': '',
            'oss_bucket_name': '',
            'oss_bucket_domain': '',
            'oss_https_enabled': False,
            'oss_custom_domain': '',
            'local_upload_path': 'uploads',
            'local_base_url': 'http://localhost:5001/uploads'
        })
    return success({
        'storage_type': config.storage_type,
        'oss_endpoint': config.oss_endpoint or '',
        'oss_access_key_id': config.oss_access_key_id or '',
        'oss_access_key_secret': config.oss_access_key_secret or '',
        'oss_bucket_name': config.oss_bucket_name or '',
        'oss_bucket_domain': config.oss_bucket_domain or '',
        'oss_https_enabled': config.oss_https_enabled or False,
        'oss_custom_domain': config.oss_custom_domain or '',
        'local_upload_path': config.local_upload_path or 'uploads',
        'local_base_url': config.local_base_url or 'http://localhost:5001/uploads'
    })

@settings_bp.route('/storage/config', methods=['PUT'])
def update_storage_config():
    """更新存储配置"""
    data = request.get_json(silent=True) or {}
    if not data:
        return error(400, '请求数据为空'), 400
    
    storage_type = data.get('storage_type', 'local')
    oss_config = data.get('oss_config') or {}
    local_upload_path = data.get('local_upload_path', 'uploads')
    local_base_url = data.get('local_base_url', 'http://localhost:5001/uploads')
    
    # 获取或创建配置
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        config = StorageConfig()
    
    # 更新配置
    config.storage_type = storage_type
    config.is_active = True
    config.local_upload_path = local_upload_path
    config.local_base_url = local_base_url
    
    if storage_type == 'oss':
        config.oss_endpoint = oss_config.get('endpoint', '')
        config.oss_access_key_id = oss_config.get('access_key_id', '')
        config.oss_access_key_secret = oss_config.get('access_key_secret', '')
        config.oss_bucket_name = oss_config.get('bucket_name', '')
        config.oss_bucket_domain = oss_config.get('bucket_domain', '')
        config.oss_https_enabled = oss_config.get('https_enabled', False)
        config.oss_custom_domain = oss_config.get('custom_domain', '')
    
    db.session.add(config)
    db.session.commit()
    
    return success({'message': '配置保存成功'})

@settings_bp.route('/settings', methods=['PUT'])
def update_settings():
    """更新系统设置"""
    data = request.get_json(silent=True) or {}
    if not data:
        return error(400, '请求数据为空'), 400
    
    for key, value in data.items():
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            new_setting = SystemSetting(setting_key=key, setting_value=value)
            db.session.add(new_setting)
    
    db.session.commit()
    return success({'message': '设置更新成功'})