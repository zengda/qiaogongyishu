from flask import Blueprint, request
from app.models.system_setting import SystemSetting
from app.models.storage_config import StorageConfig
from app.extensions import db
from app.utils.response import success, error
from app.utils.crypto import encrypt_string, decrypt_string, mask_string

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
        # 如果没有配置，返回默认值
        return success({
            'storage_type': 'local',
            'storage_config': {}
        })
    return success({
        'storage_type': config.storage_type,
        'storage_config': {
            'oss_endpoint': config.oss_endpoint,
            'oss_access_key_id': config.oss_access_key_id,
            'oss_access_key_secret': config.oss_access_key_secret,
            'oss_bucket_name': config.oss_bucket_name,
            'oss_bucket_domain': config.oss_bucket_domain,
            'oss_https_enabled': config.oss_https_enabled,
            'oss_custom_domain': config.oss_custom_domain
        }
    })

@settings_bp.route('/storage/config', methods=['PUT'])
def update_storage_config():
    """更新存储配置"""
    data = request.get_json()
    if not data:
        return error(400, '请求数据为空'), 400
    
    storage_type = data.get('storage_type', 'local')
    oss_config = data.get('oss_config', {})
    
    # 获取或创建配置
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        config = StorageConfig()
    
    # 更新配置
    config.storage_type = storage_type
    config.is_active = True
    
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
    data = request.get_json()
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

@settings_bp.route('/settings/miniprogram', methods=['GET'])
def get_miniprogram_config():
    """获取小程序配置（AppSecret脱敏显示）"""
    auth_type = SystemSetting.query.filter_by(setting_key='miniprogram_auth_type').first()
    app_id = SystemSetting.query.filter_by(setting_key='miniprogram_app_id').first()
    app_secret = SystemSetting.query.filter_by(setting_key='miniprogram_app_secret').first()
    
    # 解密AppSecret并脱敏显示
    decrypted_secret = decrypt_string(app_secret.setting_value) if app_secret else ''
    
    return success({
        'auth_type': auth_type.setting_value if auth_type else 'manual',
        'app_id': app_id.setting_value if app_id else '',
        'app_secret': mask_string(decrypted_secret)
    })

@settings_bp.route('/settings/miniprogram', methods=['PUT'])
def update_miniprogram_config():
    """更新小程序配置（AppSecret加密存储）"""
    data = request.get_json()
    if not data:
        return error(400, '请求数据为空'), 400
    
    auth_type = data.get('auth_type', 'manual')
    app_id = data.get('app_id', '').strip()
    app_secret = data.get('app_secret', '').strip()
    
    # 更新或创建配置，AppSecret需要加密存储
    settings = [
        ('miniprogram_auth_type', auth_type),
        ('miniprogram_app_id', app_id),
        ('miniprogram_app_secret', encrypt_string(app_secret))
    ]
    
    for key, value in settings:
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            new_setting = SystemSetting(setting_key=key, setting_value=value)
            db.session.add(new_setting)
    
    db.session.commit()
    return success({'message': '配置保存成功'})

@settings_bp.route('/settings/miniprogram/sync', methods=['POST'])
def sync_miniprogram_config():
    """同步配置到小程序"""
    data = request.get_json()
    if not data:
        return error(400, '请求数据为空'), 400
    
    import json
    import os
    
    # 构建小程序配置文件路径
    miniprogram_config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'miniprogram', 'utils', 'config.js'
    )
    
    # 使用JSON序列化避免注入风险
    config_data = {
        'apiBaseUrl': 'http://localhost:5001/api/v1',
        'categoryNames': ['一层', '二层', '三层', '多层', '双拼'],
        'tagNames': ['全部', '新中式', '欧式', '现代', '中式'],
        'statusMap': {
            'new': '新客户',
            'contacted': '已联系',
            'followed': '跟进中',
            'closed': '已成交'
        },
        'wechat': {
            'appId': data.get('app_id', '').strip(),
            'appSecret': data.get('app_secret', '').strip()
        }
    }
    
    # 生成配置文件内容
    config_json = json.dumps(config_data, ensure_ascii=False, indent=2)
    config_content = f'''module.exports = {config_json}
'''
    
    try:
        with open(miniprogram_config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # 同时保存到数据库（AppSecret加密存储）
        settings = [
            ('miniprogram_auth_type', data.get('auth_type', 'manual')),
            ('miniprogram_app_id', data.get('app_id', '').strip()),
            ('miniprogram_app_secret', encrypt_string(data.get('app_secret', '').strip()))
        ]
        
        for key, value in settings:
            setting = SystemSetting.query.filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = value
            else:
                new_setting = SystemSetting(setting_key=key, setting_value=value)
                db.session.add(new_setting)
        
        db.session.commit()
        
        return success({'message': '同步成功，小程序配置已更新'})
    except Exception as e:
        return error(500, f'同步失败: {str(e)}'), 500