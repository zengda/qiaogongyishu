from flask import Blueprint, request
from app.models.category import Category
from app.models.tag import Tag
from app.models.banner import Banner
from app.models.system_setting import SystemSetting
from app.models.storage_config import StorageConfig
from app.services.product_service import ProductService
from app.services.customer_service import CustomerService
from app.services.cache_service import CacheService
from app.services.storage import reset_storage_backend
from app.extensions import db
from app.utils.response import success, error, paginated
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """获取仪表盘数据"""
    stats = CustomerService.get_statistics()
    return success(stats)

@admin_bp.route('/products', methods=['GET'])
@admin_required
def admin_get_products():
    """管理后台获取产品列表"""
    keyword = request.args.get('keyword')
    category_id = request.args.get('category_id')
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    query = ProductService.get_product_list_raw(
        keyword=keyword,
        category_id=category_id,
        status=status,
        page=page,
        per_page=per_page
    )
    return success(query)

@admin_bp.route('/products', methods=['POST'])
@admin_required
def admin_create_product():
    """创建产品"""
    data = request.get_json()
    product = ProductService.create_product(data)
    if not product:
        return error(400, '创建失败'), 400
    CacheService.clear_cache('products')
    return success(product)

@admin_bp.route('/products/<int:product_id>', methods=['GET'])
@admin_required
def admin_get_product(product_id):
    """获取产品详情"""
    product = ProductService.get_product_detail(product_id)
    if not product:
        return error(404, '产品不存在'), 404
    return success(product)

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def admin_update_product(product_id):
    """更新产品"""
    data = request.get_json()
    product = ProductService.update_product(product_id, data)
    if not product:
        return error(404, '产品不存在'), 404
    CacheService.clear_cache('products')
    return success(product)

@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def admin_delete_product(product_id):
    """删除产品"""
    success_flag = ProductService.delete_product(product_id)
    if not success_flag:
        return error(404, '产品不存在'), 404
    CacheService.clear_cache('products')
    return success(message='删除成功')

@admin_bp.route('/categories', methods=['GET'])
@admin_required
def admin_get_categories():
    """获取分类列表"""
    categories = Category.query.order_by(Category.sort_order).all()
    return success([cat.to_dict() for cat in categories])

@admin_bp.route('/categories', methods=['POST'])
@admin_required
def admin_create_category():
    """创建分类"""
    data = request.get_json()
    name = data.get('name')
    if not name:
        return error(400, '分类名称不能为空'), 400
    
    if Category.query.filter_by(name=name).first():
        return error(400, '分类名称已存在'), 400
    
    category = Category(name=name, sort_order=data.get('sort_order', 0))
    db.session.add(category)
    db.session.commit()
    CacheService.clear_cache('categories')
    return success(category.to_dict())

@admin_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def admin_update_category(category_id):
    """更新分类"""
    category = Category.query.get(category_id)
    if not category:
        return error(404, '分类不存在'), 404
    
    data = request.get_json()
    if 'name' in data:
        existing = Category.query.filter_by(name=data['name']).first()
        if existing and existing.id != category_id:
            return error(400, '分类名称已存在'), 400
        category.name = data['name']
    if 'sort_order' in data:
        category.sort_order = data['sort_order']
    
    db.session.commit()
    CacheService.clear_cache('categories')
    return success(category.to_dict())

@admin_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def admin_delete_category(category_id):
    """删除分类"""
    from app.models.product import Product
    category = Category.query.get(category_id)
    if not category:
        return error(404, '分类不存在'), 404
    
    if Product.query.filter_by(category_id=category_id).first():
        return error(400, '该分类下有产品，无法删除'), 400
    
    db.session.delete(category)
    db.session.commit()
    CacheService.clear_cache('categories')
    return success(message='删除成功')

@admin_bp.route('/tags', methods=['GET'])
@admin_required
def admin_get_tags():
    """获取标签列表"""
    tags = Tag.query.order_by(Tag.sort_order).all()
    return success([t.to_dict() for t in tags])

@admin_bp.route('/tags', methods=['POST'])
@admin_required
def admin_create_tag():
    """创建标签"""
    data = request.get_json()
    name = data.get('name')
    if not name:
        return error(400, '标签名称不能为空'), 400
    
    if Tag.query.filter_by(name=name).first():
        return error(400, '标签名称已存在'), 400
    
    tag = Tag(name=name, sort_order=data.get('sort_order', 0))
    db.session.add(tag)
    db.session.commit()
    CacheService.clear_cache('tags')
    return success(tag.to_dict())

@admin_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@admin_required
def admin_update_tag(tag_id):
    """更新标签"""
    tag = Tag.query.get(tag_id)
    if not tag:
        return error(404, '标签不存在'), 404
    
    data = request.get_json()
    if 'name' in data:
        existing = Tag.query.filter_by(name=data['name']).first()
        if existing and existing.id != tag_id:
            return error(400, '标签名称已存在'), 400
        tag.name = data['name']
    if 'sort_order' in data:
        tag.sort_order = data['sort_order']
    
    db.session.commit()
    CacheService.clear_cache('tags')
    return success(tag.to_dict())

@admin_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@admin_required
def admin_delete_tag(tag_id):
    """删除标签"""
    from app.models.product_tag import ProductTag
    tag = Tag.query.get(tag_id)
    if not tag:
        return error(404, '标签不存在'), 404
    
    if ProductTag.query.filter_by(tag_id=tag_id).first():
        return error(400, '该标签下有产品，无法删除'), 400
    
    db.session.delete(tag)
    db.session.commit()
    CacheService.clear_cache('tags')
    return success(message='删除成功')

@admin_bp.route('/banners', methods=['GET'])
@admin_required
def admin_get_banners():
    """获取Banner列表"""
    banners = Banner.query.order_by(Banner.sort_order).all()
    return success([b.to_dict() for b in banners])

@admin_bp.route('/banners', methods=['POST'])
@admin_required
def admin_create_banner():
    """创建Banner"""
    data = request.get_json()
    if not data.get('image_url'):
        return error(400, '图片URL不能为空'), 400
    
    banner = Banner(
        title=data.get('title'),
        image_url=data['image_url'],
        link_type=data.get('link_type', 'none'),
        link_value=data.get('link_value'),
        sort_order=data.get('sort_order', 0),
        is_active=data.get('is_active', True),
        start_time=data.get('start_time'),
        end_time=data.get('end_time')
    )
    db.session.add(banner)
    db.session.commit()
    CacheService.clear_cache('banners')
    return success(banner.to_dict())

@admin_bp.route('/banners/<int:banner_id>', methods=['PUT'])
@admin_required
def admin_update_banner(banner_id):
    """更新Banner"""
    banner = Banner.query.get(banner_id)
    if not banner:
        return error(404, 'Banner不存在'), 404
    
    data = request.get_json()
    if 'title' in data:
        banner.title = data['title']
    if 'image_url' in data:
        banner.image_url = data['image_url']
    if 'link_type' in data:
        banner.link_type = data['link_type']
    if 'link_value' in data:
        banner.link_value = data['link_value']
    if 'sort_order' in data:
        banner.sort_order = data['sort_order']
    if 'is_active' in data:
        banner.is_active = data['is_active']
    if 'start_time' in data:
        banner.start_time = data['start_time']
    if 'end_time' in data:
        banner.end_time = data['end_time']
    
    db.session.commit()
    CacheService.clear_cache('banners')
    return success(banner.to_dict())

@admin_bp.route('/banners/<int:banner_id>', methods=['DELETE'])
@admin_required
def admin_delete_banner(banner_id):
    """删除Banner"""
    banner = Banner.query.get(banner_id)
    if not banner:
        return error(404, 'Banner不存在'), 404
    
    db.session.delete(banner)
    db.session.commit()
    CacheService.clear_cache('banners')
    return success(message='删除成功')

@admin_bp.route('/customers', methods=['GET'])
@admin_required
def admin_get_customers():
    """获取客户列表"""
    keyword = request.args.get('keyword')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    items, total, page, per_page = CustomerService.get_customer_list(
        keyword=keyword,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=page,
        per_page=per_page
    )
    
    return success(paginated(items, page, per_page, total))

@admin_bp.route('/customers/<int:customer_id>', methods=['GET'])
@admin_required
def admin_get_customer(customer_id):
    """获取客户详情"""
    customer = CustomerService.get_customer_detail(customer_id)
    if not customer:
        return error(404, '客户不存在'), 404
    return success(customer)

@admin_bp.route('/customers/<int:customer_id>/status', methods=['PATCH'])
@admin_required
def admin_update_customer_status(customer_id):
    """更新客户状态"""
    data = request.get_json()
    status = data.get('status')
    if not status:
        return error(400, '请提供状态'), 400
    
    customer = CustomerService.update_customer_status(customer_id, status)
    if not customer:
        return error(404, '客户不存在'), 404
    return success(customer)

@admin_bp.route('/customers/<int:customer_id>/remark', methods=['PATCH'])
@admin_required
def admin_update_customer_remark(customer_id):
    """更新客户备注"""
    data = request.get_json()
    remark = data.get('remark')
    
    customer = CustomerService.update_customer_remark(customer_id, remark)
    if not customer:
        return error(404, '客户不存在'), 404
    return success(customer)

@admin_bp.route('/customers/export', methods=['GET'])
@admin_required
def admin_export_customers():
    """导出客户Excel"""
    from io import BytesIO
    from openpyxl import Workbook
    from flask import send_file
    
    keyword = request.args.get('keyword')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    customers, _, _, _ = CustomerService.get_customer_list(
        keyword=keyword,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=1,
        per_page=9999
    )
    
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', '姓名', '手机号', '微信号', '省份', '城市', '建房面积预算', '意向产品', '状态', '提交时间'])
    
    for c in customers:
        ws.append([
            c['id'],
            c['name'],
            c['phone'],
            c['wechat'] or '',
            c['province'] or '',
            c['city'] or '',
            c['building_area_budget'] or '',
            c['product_title'] or '',
            c['status'],
            c['created_at']
        ])
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='customers.xlsx'
    )

@admin_bp.route('/settings', methods=['GET'])
@admin_required
def admin_get_settings():
    """获取所有系统设置"""
    settings = SystemSetting.query.all()
    result = {}
    for s in settings:
        result[s.setting_key] = s.setting_value
    return success(result)

@admin_bp.route('/settings', methods=['PUT'])
@admin_required
def admin_update_settings():
    """更新系统设置"""
    data = request.get_json()
    for key, value in data.items():
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            setting = SystemSetting(setting_key=key, setting_value=value)
            db.session.add(setting)
    db.session.commit()
    return success(message='更新成功')

@admin_bp.route('/storage/config', methods=['GET'])
@admin_required
def admin_get_storage_config():
    """获取存储配置"""
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        return error(404, '存储配置不存在'), 404
    return success(config.to_dict(include_secret=True))

@admin_bp.route('/storage/config', methods=['PUT'])
@admin_required
def admin_update_storage_config():
    """更新存储配置"""
    data = request.get_json()
    
    active_config = StorageConfig.query.filter_by(is_active=True).first()
    if active_config:
        active_config.is_active = False
    
    new_config = StorageConfig(
        storage_type=data.get('storage_type', 'local'),
        local_base_url=data.get('local_base_url'),
        local_upload_path=data.get('local_upload_path'),
        oss_access_key_id=data.get('oss_access_key_id'),
        oss_access_key_secret=data.get('oss_access_key_secret'),
        oss_bucket_name=data.get('oss_bucket_name'),
        oss_endpoint=data.get('oss_endpoint'),
        oss_cdn_domain=data.get('oss_cdn_domain'),
        oss_custom_domain=data.get('oss_custom_domain'),
        oss_region=data.get('oss_region'),
        max_file_size=data.get('max_file_size', 5242880),
        allowed_extensions=data.get('allowed_extensions', 'jpg,jpeg,png,webp,gif'),
        is_active=True
    )
    
    db.session.add(new_config)
    db.session.commit()
    reset_storage_backend()
    return success(new_config.to_dict(include_secret=True))