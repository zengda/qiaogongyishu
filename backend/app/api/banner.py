from flask import Blueprint, request
from app.services.cache_service import CacheService
from app.utils.response import success, error

banner_bp = Blueprint('banner', __name__)

@banner_bp.route('/banners', methods=['GET'])
def get_banners():
    """获取Banner列表"""
    banners = CacheService.get_banners()
    return success(banners)