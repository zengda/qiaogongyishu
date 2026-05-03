import json
from app.models.category import Category
from app.models.tag import Tag
from app.models.banner import Banner

class CacheService:
    """缓存服务"""
    
    @staticmethod
    def _get_redis():
        """延迟获取 redis_client，避免 Flask 调试模式下模块重新加载的问题"""
        from app.extensions import redis_client
        return redis_client
    
    @staticmethod
    def get_categories():
        """获取分类缓存"""
        key = 'categories'
        redis_client = CacheService._get_redis()
        
        if redis_client:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        
        categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
        result = [cat.to_dict() for cat in categories]
        
        if redis_client:
            redis_client.setex(key, 3600, json.dumps(result))
        return result
    
    @staticmethod
    def get_tags():
        """获取标签缓存"""
        key = 'tags'
        redis_client = CacheService._get_redis()
        
        if redis_client:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        
        tags = Tag.query.filter_by(is_active=True).order_by(Tag.sort_order).all()
        result = [tag.to_dict() for tag in tags]
        
        if redis_client:
            redis_client.setex(key, 3600, json.dumps(result))
        return result
    
    @staticmethod
    def get_banners():
        """获取Banner缓存"""
        key = 'banners'
        redis_client = CacheService._get_redis()
        
        if redis_client:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        
        banners = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order).all()
        result = [banner.to_dict() for banner in banners if banner.is_valid()]
        
        if redis_client:
            redis_client.setex(key, 1800, json.dumps(result))
        return result
    
    @staticmethod
    def clear_cache(prefix=None):
        """清除缓存"""
        redis_client = CacheService._get_redis()
        if not redis_client:
            return
        
        if prefix:
            keys = list(redis_client.keys(f'{prefix}:*'))
            keys.append(prefix)
        else:
            keys = list(redis_client.keys('*'))
        if keys:
            redis_client.delete(*keys)