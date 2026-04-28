"""加密工具类"""
from cryptography.fernet import Fernet
import os
from app.extensions import db
from app.models.system_setting import SystemSetting

# 加密密钥管理
ENCRYPTION_KEY_SETTING_KEY = 'encryption_key'

def get_encryption_key():
    """获取或生成加密密钥"""
    # 尝试从数据库获取密钥
    key_setting = SystemSetting.query.filter_by(setting_key=ENCRYPTION_KEY_SETTING_KEY).first()
    
    if key_setting and key_setting.setting_value:
        return key_setting.setting_value.encode('utf-8')
    
    # 如果没有密钥，生成新密钥并保存
    new_key = Fernet.generate_key()
    new_setting = SystemSetting(
        setting_key=ENCRYPTION_KEY_SETTING_KEY,
        setting_value=new_key.decode('utf-8'),
        description='加密密钥（自动生成）'
    )
    db.session.add(new_setting)
    db.session.commit()
    
    return new_key

def encrypt_string(value):
    """加密字符串"""
    if not value:
        return value
    
    try:
        key = get_encryption_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(value.encode('utf-8'))
        return encrypted.decode('utf-8')
    except Exception as e:
        # 如果加密失败，返回原始值（降级处理）
        return value

def decrypt_string(value):
    """解密字符串"""
    if not value:
        return value
    
    try:
        key = get_encryption_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(value.encode('utf-8'))
        return decrypted.decode('utf-8')
    except Exception as e:
        # 如果解密失败，返回原始值（可能是未加密的旧数据）
        return value

def mask_string(value, keep_length=8):
    """脱敏显示字符串，保留最后keep_length位"""
    if not value:
        return ''
    if len(value) <= keep_length:
        return '*' * len(value)
    return '*' * (len(value) - keep_length) + value[-keep_length:]