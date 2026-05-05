from app.services.storage import get_storage_backend
from app.models.storage_config import StorageConfig
from app.config import Config

class UploadService:
    """上传服务"""

    DEFAULT_MAX_FILE_SIZE = Config.MAX_FILE_SIZE

    @staticmethod
    def upload_image(file):
        """上传图片文件"""
        if not file:
            return None, '未提供文件'

        filename = file.filename
        if not filename or not UploadService._allowed_file(filename):
            return None, '文件格式不允许'

        config = StorageConfig.query.filter_by(is_active=True).first()
        max_size = config.max_file_size if config else UploadService.DEFAULT_MAX_FILE_SIZE

        file_size = UploadService._get_file_size(file)
        if file_size is not None and file_size > max_size:
            return None, f'文件大小超过限制（最大{max_size / 1024 / 1024}MB）'
        
        try:
            storage = get_storage_backend()
            url = storage.upload(file, filename)
            return url, None
        except Exception as e:
            return None, f'上传失败：{str(e)}'
    
    @staticmethod
    def _get_file_size(file):
        size = file.content_length
        if size is not None:
            return size
        try:
            file.stream.seek(0, 2)
            size = file.stream.tell()
            file.stream.seek(0)
            return size
        except Exception:
            return None

    @staticmethod
    def _allowed_file(filename):
        """检查文件格式是否允许"""
        config = StorageConfig.query.filter_by(is_active=True).first()
        if config:
            allowed = config.allowed_extensions.split(',')
        else:
            allowed = ['jpg', 'jpeg', 'png', 'webp', 'gif']
        
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() in allowed