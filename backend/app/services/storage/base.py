from abc import ABC, abstractmethod

class StorageBackend(ABC):
    """存储服务抽象基类"""
    
    @abstractmethod
    def upload(self, file, filename):
        """上传文件"""
        pass
    
    @abstractmethod
    def delete(self, file_path):
        """删除文件"""
        pass
    
    @abstractmethod
    def get_url(self, filename):
        """获取文件访问URL"""
        pass