import uuid
from oss2 import Auth, Bucket
from app.services.storage.base import StorageBackend

class OSSStorage(StorageBackend):
    """阿里云OSS存储实现"""
    
    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint, 
                 cdn_domain=None, custom_domain=None, bucket_domain=None, https_enabled=False):
        self.auth = Auth(access_key_id, access_key_secret)
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.cdn_domain = cdn_domain
        self.custom_domain = custom_domain
        self.bucket_domain = bucket_domain
        self.https_enabled = https_enabled
        
        # 根据 HTTPS 配置选择协议
        protocol = 'https' if https_enabled else 'http'
        if bucket_domain:
            bucket_url = f"{protocol}://{bucket_domain}"
        else:
            bucket_url = f"{protocol}://{endpoint}"
        self.bucket = Bucket(self.auth, bucket_url, bucket_name) if not (bucket_domain or '').startswith(bucket_name + '.') else Bucket(self.auth, bucket_url)
    
    def upload(self, file, filename):
        ext = filename.rsplit('.', 1)[-1].lower()
        new_filename = f"uploads/{uuid.uuid4().hex}.{ext}"
        file.seek(0)
        self.bucket.put_object(new_filename, file.read())
        return self.get_url(new_filename)
    
    def delete(self, file_path):
        try:
            self.bucket.delete_object(file_path)
            return True
        except Exception:
            return False
    
    def get_url(self, filename):
        protocol = 'https' if self.https_enabled else 'http'
        if self.cdn_domain:
            return f"{protocol}://{self.cdn_domain}/{filename}"
        elif self.custom_domain:
            return f"{protocol}://{self.custom_domain}/{filename}"
        elif self.bucket_domain:
            return f"{protocol}://{self.bucket_domain}/{filename}"
        else:
            return f"{protocol}://{self.bucket_name}.{self.endpoint}/{filename}"