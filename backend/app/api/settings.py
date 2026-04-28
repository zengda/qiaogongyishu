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
    """获取存储配置（公开）"""
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        return error(404, '存储配置不存在'), 404
    return success({'storage_type': config.storage_type})

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