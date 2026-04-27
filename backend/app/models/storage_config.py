from app.extensions import db
from datetime import datetime

class StorageConfig(db.Model):
    __tablename__ = 'storage_configs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    storage_type = db.Column(db.Enum('local', 'oss'), nullable=False, default='local')
    local_base_url = db.Column(db.String(500))
    local_upload_path = db.Column(db.String(500))
    oss_access_key_id = db.Column(db.String(200))
    oss_access_key_secret = db.Column(db.String(500))
    oss_bucket_name = db.Column(db.String(200))
    oss_endpoint = db.Column(db.String(500))
    oss_cdn_domain = db.Column(db.String(500))
    oss_custom_domain = db.Column(db.String(500))
    oss_region = db.Column(db.String(100))
    max_file_size = db.Column(db.Integer, default=5242880)
    allowed_extensions = db.Column(db.String(500), default='jpg,jpeg,png,webp,gif')
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self, include_secret=False):
        result = {
            'id': self.id,
            'storage_type': self.storage_type,
            'local_base_url': self.local_base_url,
            'local_upload_path': self.local_upload_path,
            'oss_access_key_id': self.oss_access_key_id,
            'oss_bucket_name': self.oss_bucket_name,
            'oss_endpoint': self.oss_endpoint,
            'oss_cdn_domain': self.oss_cdn_domain,
            'oss_custom_domain': self.oss_custom_domain,
            'oss_region': self.oss_region,
            'max_file_size': self.max_file_size,
            'allowed_extensions': self.allowed_extensions,
            'is_active': self.is_active,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        if include_secret:
            result['oss_access_key_secret'] = self.oss_access_key_secret
        else:
            if self.oss_access_key_secret:
                result['oss_access_key_secret'] = self.oss_access_key_secret[:6] + '*' * 10 + self.oss_access_key_secret[-4:]
            else:
                result['oss_access_key_secret'] = None
        return result