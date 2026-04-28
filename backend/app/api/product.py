from flask import Blueprint, request
from app.services.product_service import ProductService
from app.utils.response import success, error, paginated

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    """获取产品列表"""
    category_id = request.args.get('category_id')
    tag_id = request.args.get('tag_id')
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    items, total, page, per_page = ProductService.get_product_list(
        category_id=category_id,
        tag_id=tag_id,
        keyword=keyword,
        page=page,
        per_page=per_page
    )
    
    return success(paginated(items, page, per_page, total))

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    """获取产品详情"""
    product = ProductService.get_product_detail(product_id)
    if not product:
        return error(404, '产品不存在'), 404
    return success(product)

@product_bp.route('/products/<int:product_id>/view', methods=['POST'])
def record_product_view(product_id):
    """记录产品浏览"""
    success_flag = ProductService.increment_view_count(product_id)
    if not success_flag:
        return error(404, '产品不存在'), 404
    return success(message='记录成功')

@product_bp.route('/search', methods=['GET'])
def search_products():
    """搜索产品"""
    keyword = request.args.get('keyword')
    if not keyword:
        return error(400, '请提供搜索关键词'), 400
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    items, total, page, per_page = ProductService.get_product_list(
        keyword=keyword,
        page=page,
        per_page=per_page
    )
    
    return success(paginated(items, page, per_page, total))