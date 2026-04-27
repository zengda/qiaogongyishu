import uuid
from oss2 import Auth, Bucket
from app.services.storage.base import StorageBackend

class OSSStorage(StorageBackend):
    """阿里云OSS存储实现"""
    
    def __init__(self, access_key_id, access_key_secret, bucket_name, endpoint, cdn_domain=None, custom_domain=None):
        self.auth = Auth(access_key_id, access_key_secret)
        self.bucket = Bucket(self.auth, endpoint, bucket_name)
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.cdn_domain = cdn_domain
        self.custom_domain = custom_domain
    
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
        if self.cdn_domain:
            return f"{self.cdn_domain}/{filename}"
        elif self.custom_domain:
            return f"{self.custom_domain}/{filename}"
        else:
            return f"https://{self.bucket_name}.{self.endpoint}/{filename}"