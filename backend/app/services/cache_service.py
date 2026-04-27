from app.extensions import redis_client
from app.models.category import Category
from app.models.tag import Tag
from app.models.banner import Banner

class CacheService:
    """缓存服务"""
    
    @staticmethod
    def get_categories():
        """获取分类缓存"""
        key = 'categories'
        data = redis_client.get(key)
        if data:
            import json
            return json.loads(data)
        
        categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
        result = [cat.to_dict() for cat in categories]
        
        redis_client.setex(key, 3600, json.dumps(result))
        return result
    
    @staticmethod
    def get_tags():
        """获取标签缓存"""
        key = 'tags'
        data = redis_client.get(key)
        if data:
            import json
            return json.loads(data)
        
        tags = Tag.query.filter_by(is_active=True).order_by(Tag.sort_order).all()
        result = [tag.to_dict() for tag in tags]
        
        redis_client.setex(key, 3600, json.dumps(result))
        return result
    
    @staticmethod
    def get_banners():
        """获取Banner缓存"""
        key = 'banners'
        data = redis_client.get(key)
        if data:
            import json
            return json.loads(data)
        
        banners = Banner.query.filter_by(is_active=True).order_by(Banner.sort_order).all()
        result = [banner.to_dict() for banner in banners if banner.is_valid()]
        
        redis_client.setex(key, 1800, json.dumps(result))
        return result
    
    @staticmethod
    def clear_cache(prefix=None):
        """清除缓存"""
        if prefix:
            keys = redis_client.keys(f'{prefix}:*')
        else:
            keys = redis_client.keys('*')
        if keys:
            redis_client.delete(*keys)