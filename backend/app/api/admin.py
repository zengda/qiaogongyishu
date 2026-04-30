from flask import Blueprint, request
from datetime import datetime, timedelta
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
    try:
        from app.models.product import Product
        from app.models.banner import Banner
        from app.models.customer import Customer
        
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        week_ago = today - timedelta(days=7)
        week_start = datetime.combine(week_ago, datetime.min.time())
        
        month_ago = today - timedelta(days=30)
        month_start = datetime.combine(month_ago, datetime.min.time())
        
        product_count = Product.query.count()
        customer_today = Customer.query.filter(Customer.created_at.between(today_start, today_end)).count()
        customer_week = Customer.query.filter(Customer.created_at >= week_start).count()
        customer_month = Customer.query.filter(Customer.created_at >= month_start).count()
        customer_total = Customer.query.count()
        banner_count = Banner.query.filter_by(is_active=True).count()
        
        stats = {
            'productCount': product_count,
            'customerCount': customer_total,
            'customerToday': customer_today,
            'customerWeek': customer_week,
            'customerMonth': customer_month,
            'viewCount': 0,
            'bannerCount': banner_count
        }
        
        return success(stats)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error(500, str(e)), 500

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
    data = request.get_json(silent=True) or {}
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
    data = request.get_json(silent=True) or {}
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

@admin_bp.route('/categories/<int:category_id>', methods=['GET'])
@admin_required
def admin_get_category(category_id):
    """获取单个分类"""
    category = Category.query.get(category_id)
    if not category:
        return error(404, '分类不存在'), 404
    return success(category.to_dict())

@admin_bp.route('/categories', methods=['POST'])
@admin_required
def admin_create_category():
    """创建分类"""
    data = request.get_json(silent=True) or {}
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
    
    data = request.get_json(silent=True) or {}
    if 'name' in data:
        existing = Category.query.filter_by(name=data['name']).first()
        if existing and existing.id != category_id:
            return error(400, '分类名称已存在'), 400
        category.name = data['name']
    if 'sort_order' in data:
        category.sort_order = data['sort_order']
    if 'is_active' in data:
        category.is_active = data['is_active']
    
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

@admin_bp.route('/tags/<int:tag_id>', methods=['GET'])
@admin_required
def admin_get_tag(tag_id):
    """获取单个标签"""
    tag = Tag.query.get(tag_id)
    if not tag:
        return error(404, '标签不存在'), 404
    return success(tag.to_dict())

@admin_bp.route('/tags', methods=['POST'])
@admin_required
def admin_create_tag():
    """创建标签"""
    data = request.get_json(silent=True) or {}
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
    
    data = request.get_json(silent=True) or {}
    if 'name' in data:
        existing = Tag.query.filter_by(name=data['name']).first()
        if existing and existing.id != tag_id:
            return error(400, '标签名称已存在'), 400
        tag.name = data['name']
    if 'sort_order' in data:
        tag.sort_order = data['sort_order']
    if 'is_active' in data:
        tag.is_active = data['is_active']
    
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
    data = request.get_json(silent=True) or {}
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

@admin_bp.route('/banners/<int:banner_id>', methods=['GET'])
@admin_required
def admin_get_banner(banner_id):
    """获取单个Banner详情"""
    banner = Banner.query.get(banner_id)
    if not banner:
        return error(404, 'Banner不存在'), 404
    return success(banner.to_dict())

@admin_bp.route('/banners/<int:banner_id>', methods=['PUT'])
@admin_required
def admin_update_banner(banner_id):
    """更新Banner"""
    banner = Banner.query.get(banner_id)
    if not banner:
        return error(404, 'Banner不存在'), 404
    
    data = request.get_json(silent=True) or {}
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

@admin_bp.route('/customers', methods=['POST'])
@admin_required
def admin_create_customer():
    """创建客户"""
    data = request.get_json(silent=True) or {}
    
    if not data.get('name') or not data.get('phone'):
        return error(400, '姓名和手机号为必填项'), 400
    
    customer, err = CustomerService.create_customer(data)
    if err:
        return error(400, err), 400
    
    return success(customer)

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
    data = request.get_json(silent=True) or {}
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
    data = request.get_json(silent=True) or {}
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

@admin_bp.route('/settings/<string:key>', methods=['GET'])
@admin_required
def admin_get_setting(key):
    """获取单个系统设置"""
    setting = SystemSetting.query.filter_by(setting_key=key).first()
    if not setting:
        return success({'value': ''})
    return success({'value': setting.setting_value})

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
    data = request.get_json(silent=True) or {}
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
    data = request.get_json(silent=True) or {}
    
    oss_config = data.get('oss_config', {})
    storage_type = data.get('storage_type', oss_config.get('storage_type', 'local'))
    
    active_config = StorageConfig.query.filter_by(is_active=True).first()
    if not active_config:
        active_config = StorageConfig()
    
    active_config.is_active = True
    active_config.storage_type = storage_type
    
    if storage_type == 'oss':
        active_config.oss_endpoint = oss_config.get('endpoint') or data.get('oss_endpoint', '')
        active_config.oss_access_key_id = oss_config.get('access_key_id') or data.get('oss_access_key_id', '')
        active_config.oss_access_key_secret = oss_config.get('access_key_secret') or data.get('oss_access_key_secret', '')
        active_config.oss_bucket_name = oss_config.get('bucket_name') or data.get('oss_bucket_name', '')
        active_config.oss_bucket_domain = oss_config.get('bucket_domain') or data.get('oss_bucket_domain', '')
        active_config.oss_https_enabled = oss_config.get('https_enabled') or data.get('oss_https_enabled', False)
        active_config.oss_cdn_domain = oss_config.get('cdn_domain') or data.get('oss_cdn_domain', '')
        active_config.oss_custom_domain = oss_config.get('custom_domain') or data.get('oss_custom_domain', '')
        active_config.oss_region = oss_config.get('region') or data.get('oss_region', '')
    else:
        active_config.local_upload_path = data.get('local_upload_path', 'uploads')
        active_config.local_base_url = data.get('local_base_url', 'http://localhost:5001/uploads')
    
    db.session.commit()
    reset_storage_backend()
    return success(active_config.to_dict(include_secret=True))


@admin_bp.route('/storage/migrate-to-oss', methods=['POST'])
@admin_required
def migrate_local_files_to_oss():
    """将本地 uploads 目录中的文件迁移到 OSS"""
    from app.services.storage import LocalStorage, get_storage_backend
    import os
    
    config = StorageConfig.query.filter_by(is_active=True).first()
    if not config:
        return error(400, '请先配置存储服务'), 400
    if config.storage_type != 'oss':
        return error(400, '当前存储方式不是 OSS，请先切换到 OSS 后再执行迁移'), 400
    
    local_path = config.local_upload_path
    if not os.path.isabs(local_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        local_path = os.path.join(os.path.dirname(base_dir), local_path)
    
    if not os.path.exists(local_path):
        return error(400, f'本地上传目录不存在: {local_path}'), 400
    
    local_storage = LocalStorage(
        upload_path=local_path,
        base_url=config.local_base_url or ''
    )
    
    files = local_storage.list_files()
    if not files:
        return success({'message': '没有需要迁移的文件', 'migrated': 0, 'total': 0, 'failed': 0})
    
    oss_storage = get_storage_backend()
    
    migrated = []
    failed_list = []
    
    for file_info in files:
        local_file_path = file_info['path']
        filename = file_info['filename']
        
        try:
            class LocalFile:
                def __init__(self, path, name):
                    self.filename = name
                    self._path = path
                def seek(self, _offset):
                    pass
                def read(self):
                    with open(self._path, 'rb') as f:
                        return f.read()
                @property
                def content_length(self):
                    return os.path.getsize(self._path)
            
            file_obj = LocalFile(local_file_path, filename)
            new_url = oss_storage.upload(file_obj, filename)
            migrated.append({
                'filename': filename,
                'old_url': file_info['url'],
                'new_url': new_url
            })
        except Exception as e:
            failed_list.append({
                'filename': filename,
                'error': str(e)
            })
    
    return success({
        'migrated': len(migrated),
        'total': len(files),
        'failed': len(failed_list),
        'migrated_files': migrated,
        'failed_files': failed_list
    })

@admin_bp.route('/profile/password', methods=['PUT'])
@admin_required
def admin_change_password():
    """修改密码"""
    from app.models.admin import Admin
    from werkzeug.security import check_password_hash, generate_password_hash
    
    data = request.get_json(silent=True) or {}
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return error(400, '请提供当前密码和新密码'), 400
    
    # 获取当前管理员
    admin_user = Admin.query.filter_by(username='admin').first()
    if not admin_user:
        return error(404, '管理员不存在'), 404
    
    # 验证当前密码
    if not check_password_hash(admin_user.password_hash, old_password):
        return error(400, '当前密码错误'), 400
    
    # 更新密码
    admin_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return success({'message': '密码修改成功'})

@admin_bp.route('/storage/test-oss', methods=['POST'])
@admin_required
def test_oss_connection():
    """测试阿里云OSS连接"""
    from app.utils.response import error
    import oss2
    
    data = request.get_json(silent=True) or {}
    endpoint = data.get('endpoint')
    access_key_id = data.get('access_key_id')
    access_key_secret = data.get('access_key_secret')
    bucket_name = data.get('bucket_name')
    https_enabled = data.get('https_enabled', False)
    bucket_domain = data.get('bucket_domain')
    
    if not all([endpoint, access_key_id, access_key_secret, bucket_name]):
        return error(400, '缺少必要的参数'), 400
    
    try:
        auth = oss2.Auth(access_key_id, access_key_secret)
        
        # 根据 HTTPS 配置选择协议
        protocol = 'https' if https_enabled else 'http'
        if bucket_domain:
            bucket_url = f"{protocol}://{bucket_domain}"
        else:
            bucket_url = f"{protocol}://{endpoint}"
        
        bucket = oss2.Bucket(auth, bucket_url, bucket_name)
        
        # 获取Bucket信息以验证连接
        bucket_info = bucket.get_bucket_info()
        
        result = {
            'message': 'OSS 连接测试成功',
            'bucket_name': bucket_name,
            'bucket_region': bucket_info.bucket.location if hasattr(bucket_info, 'location') else 'unknown',
            'storage_size': bucket_info.bucket.storage_size if hasattr(bucket_info, 'bucket') else 'unknown'
        }
        
        return success(result)
    except oss2.exceptions.ServerError as e:
        return error(400, f'OSS 连接失败: {str(e)}'), 400
    except oss2.exceptions.RequestError as e:
        return error(400, f'网络请求失败: {str(e)}'), 400
    except Exception as e:
        return error(400, f'连接失败: {str(e)}'), 400


@admin_bp.route('/miniprogram/config', methods=['GET'])
@admin_required
def get_miniprogram_config():
    """获取小程序配置"""
    keys = [
        'miniprogram_appid',
        'miniprogram_private_key',
        'miniprogram_project_path',
        'miniprogram_type',
        'miniprogram_robot',
        'miniprogram_latest_version',
        'miniprogram_latest_desc'
    ]
    result = {}
    for key in keys:
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        result[key.replace('miniprogram_', '')] = setting.setting_value if setting else ''
    return success(result)


@admin_bp.route('/miniprogram/config', methods=['PUT'])
@admin_required
def update_miniprogram_config():
    """保存小程序配置"""
    data = request.get_json(silent=True) or {}
    mappings = {
        'appid': 'miniprogram_appid',
        'private_key': 'miniprogram_private_key',
        'project_path': 'miniprogram_project_path',
        'type': 'miniprogram_type',
        'robot': 'miniprogram_robot'
    }
    for field, setting_key in mappings.items():
        value = data.get(field)
        if value is not None:
            setting = SystemSetting.query.filter_by(setting_key=setting_key).first()
            if setting:
                setting.setting_value = str(value)
            else:
                db.session.add(SystemSetting(setting_key=setting_key, setting_value=str(value)))
    db.session.commit()
    return success(message='小程序配置保存成功')


@admin_bp.route('/miniprogram/preview', methods=['POST'])
@admin_required
def miniprogram_preview():
    """小程序预览"""
    import subprocess, os, uuid
    data = request.get_json(silent=True) or {}
    desc = data.get('desc', '从管理后台预览')
    page_path = data.get('page_path', 'pages/index/index')
    search_query = data.get('search_query', '')

    config = _get_miniprogram_config_dict()
    if not config.get('appid'):
        return error(400, '请先配置小程序 AppID'), 400
    if not config.get('private_key'):
        return error(400, '请先配置上传密钥'), 400
    if not config.get('project_path'):
        return error(400, '请先配置项目路径'), 400

    private_key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'private.key')
    with open(private_key_path, 'w') as f:
        f.write(config['private_key'])

    qrcode_filename = f'preview-{uuid.uuid4().hex[:8]}.jpg'
    qrcode_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads', qrcode_filename)
    robot = config.get('robot', '1')

    try:
        cmd = [
            'node', os.path.join(os.path.dirname(__file__), '..', 'scripts', 'miniprogram-ci.js'),
            'preview',
            '--appid', config['appid'],
            '--project-path', config['project_path'],
            '--private-key-path', private_key_path,
            '--desc', desc,
            '--page-path', page_path,
            '--search-query', search_query,
            '--robot', str(robot),
            '--qrcode-output', qrcode_path,
            '--qrcode-format', 'image'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if result.returncode != 0:
            return error(500, f'预览失败: {result.stderr.strip()}'), 500

        qrcode_url = f'/uploads/{qrcode_filename}'
        return success({'qrcode_url': qrcode_url})
    except subprocess.TimeoutExpired:
        return error(500, '预览超时，请重试'), 500
    except FileNotFoundError:
        return error(500, '未找到 miniprogram-ci 运行环境，请确保 Node.js 和 miniprogram-ci 已安装'), 500
    finally:
        if os.path.exists(private_key_path):
            os.remove(private_key_path)


@admin_bp.route('/miniprogram/upload', methods=['POST'])
@admin_required
def miniprogram_upload():
    """小程序上传代码"""
    import subprocess, os
    data = request.get_json(silent=True) or {}
    version = data.get('version', '').strip()
    desc = data.get('desc', '').strip()

    if not version:
        return error(400, '请输入版本号'), 400

    config = _get_miniprogram_config_dict()
    if not config.get('appid'):
        return error(400, '请先配置小程序 AppID'), 400
    if not config.get('private_key'):
        return error(400, '请先配置上传密钥'), 400
    if not config.get('project_path'):
        return error(400, '请先配置项目路径'), 400

    private_key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'private.key')
    with open(private_key_path, 'w') as f:
        f.write(config['private_key'])

    robot = config.get('robot', '1')

    try:
        cmd = [
            'node', os.path.join(os.path.dirname(__file__), '..', 'scripts', 'miniprogram-ci.js'),
            'upload',
            '--appid', config['appid'],
            '--project-path', config['project_path'],
            '--private-key-path', private_key_path,
            '--version', version,
            '--desc', desc,
            '--robot', str(robot)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if result.returncode != 0:
            return error(500, f'上传失败: {result.stderr.strip()}'), 500

        SystemSetting.query.filter_by(setting_key='miniprogram_latest_version').update(
            {'setting_value': version}
        )
        if desc:
            existing_desc = SystemSetting.query.filter_by(setting_key='miniprogram_latest_desc').first()
            if existing_desc:
                existing_desc.setting_value = desc
            else:
                db.session.add(SystemSetting(setting_key='miniprogram_latest_desc', setting_value=desc))
        db.session.commit()

        return success({
            'message': '上传成功',
            'version': version,
            'desc': desc
        })
    except subprocess.TimeoutExpired:
        return error(500, '上传超时，请重试'), 500
    except FileNotFoundError:
        return error(500, '未找到 miniprogram-ci 运行环境，请确保 Node.js 和 miniprogram-ci 已安装'), 500
    finally:
        if os.path.exists(private_key_path):
            os.remove(private_key_path)


def _get_miniprogram_config_dict():
    """从数据库读取小程序配置"""
    keys = ['miniprogram_appid', 'miniprogram_private_key', 'miniprogram_project_path',
            'miniprogram_type', 'miniprogram_robot']
    config = {}
    for key in keys:
        setting = SystemSetting.query.filter_by(setting_key=key).first()
        config[key.replace('miniprogram_', '')] = setting.setting_value if setting else ''
    return config
