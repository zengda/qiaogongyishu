from flask import Blueprint, request
from app.models.tag import Tag
from app.extensions import db
from app.utils.response import success, error

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取标签列表"""
    tags = Tag.query.filter_by(is_active=True).order_by(Tag.sort_order).all()
    return success([t.to_dict() for t in tags])