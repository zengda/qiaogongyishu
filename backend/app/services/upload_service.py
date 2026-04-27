from app.services.storage import get_storage_backend
from app.models.storage_config import StorageConfig

class UploadService:
    """上传服务"""
    
    @staticmethod
    def upload_image(file):
        """上传图片文件"""
        if not file:
            return None, '未提供文件'
        
        filename = file.filename
        if not filename or not UploadService._allowed_file(filename):
            return None, '文件格式不允许'
        
        config = StorageConfig.query.filter_by(is_active=True).first()
        if config and file.content_length > config.max_file_size:
            return None, f'文件大小超过限制（最大{config.max_file_size / 1024 / 1024}MB）'
        
        try:
            storage = get_storage_backend()
            url = storage.upload(file, filename)
            return url, None
        except Exception as e:
            return None, f'上传失败：{str(e)}'
    
    @staticmethod
    def _allowed_file(filename):
        """检查文件格式是否允许"""
        config = StorageConfig.query.filter_by(is_active=True).first()
        if config:
            allowed = config.allowed_extensions.split(',')
        else:
            allowed = ['jpg', 'jpeg', 'png', 'webp', 'gif']
        
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in allowed