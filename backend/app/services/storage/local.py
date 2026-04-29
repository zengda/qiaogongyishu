import os
import uuid
from app.services.storage.base import StorageBackend

class LocalStorage(StorageBackend):
    """本地存储实现"""
    
    def __init__(self, upload_path, base_url):
        self.upload_path = upload_path
        self.base_url = base_url
        os.makedirs(upload_path, exist_ok=True)
    
    def upload(self, file, filename):
        ext = filename.rsplit('.', 1)[-1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(self.upload_path, new_filename)
        file.save(file_path)
        return self.get_url(new_filename)
    
    def delete(self, file_path):
        full_path = os.path.join(self.upload_path, os.path.basename(file_path))
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    
    def get_url(self, filename):
        return f"{self.base_url}/{filename}"
    
    def list_files(self):
        """列出上传目录中的所有文件"""
        files = []
        if os.path.exists(self.upload_path):
            for f in os.listdir(self.upload_path):
                full_path = os.path.join(self.upload_path, f)
                if os.path.isfile(full_path):
                    files.append({
                        'filename': f,
                        'path': full_path,
                        'url': self.get_url(f),
                        'size': os.path.getsize(full_path)
                    })
        return files