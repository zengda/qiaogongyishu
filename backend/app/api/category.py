from flask import Blueprint, request
from app.models.category import Category
from app.extensions import db
from app.utils.response import success, error

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取分类列表"""
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return success([cat.to_dict() for cat in categories])