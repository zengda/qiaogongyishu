from app.extensions import db
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_tag import ProductTag
from app.models.category import Category
from app.models.tag import Tag
from app.utils.pagination import paginate
from app.utils.response import paginated

class ProductService:
    """产品服务"""
    
    @staticmethod
    def get_product_list(category_id=None, tag_id=None, keyword=None, page=1, per_page=10):
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if tag_id:
            query = query.join(ProductTag).filter(ProductTag.tag_id == tag_id)
        
        if keyword:
            query = query.filter(
                (Product.title.like(f'%{keyword}%')) |
                (Product.model_number.like(f'%{keyword}%'))
            )
        
        query = query.order_by(Product.sort_order.desc(), Product.created_at.desc())
        items, total, page, per_page = paginate(query, page, per_page)
        
        products = []
        for item in items:
            product_dict = item.to_dict()
            banner_img = next((img for img in item.images if img.image_type == 'banner'), None)
            product_dict['cover_image'] = banner_img.image_url if banner_img else None
            product_dict['tags'] = [pt.tag.name for pt in item.tags]
            products.append(product_dict)
        
        return products, total, page, per_page
    
    @staticmethod
    def get_product_detail(product_id):
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return None
        return product.to_dict(include_images=True, include_tags=True)
    
    @staticmethod
    def create_product(data):
        product = Product(
            title=data['title'],
            model_number=data['model_number'],
            category_id=data.get('category_id'),
            description=data.get('detail'),
            floor_area=data.get('floor_area'),
            building_area=data.get('building_area'),
            rooms=data.get('rooms'),
            sort_order=data.get('sort_order', 0),
            is_active=data.get('is_active', True)
        )
        db.session.add(product)
        db.session.flush()
        
        cover_image = data.get('cover_image')
        banner_images = data.get('banner_images', [])
        
        if cover_image:
            banner_images = [cover_image] + banner_images
        
        for i, img in enumerate(banner_images):
            image_url = img.image_url if hasattr(img, 'image_url') else img
            if image_url:
                db.session.add(ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    image_type='banner',
                    sort_order=i
                ))
        
        tags = data.get('tags', [])
        for tag_id in tags:
            db.session.add(ProductTag(product_id=product.id, tag_id=tag_id))
        
        db.session.commit()
        return product.to_dict(include_images=True, include_tags=True)
    
    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None
        
        if 'title' in data:
            product.title = data['title']
        if 'model_number' in data:
            product.model_number = data['model_number']
        if 'category_id' in data:
            product.category_id = data['category_id']
        if 'description' in data:
            product.description = data['description']
        if 'detail' in data:
            product.description = data['detail']
        if 'floor_area' in data:
            product.floor_area = data['floor_area']
        if 'building_area' in data:
            product.building_area = data['building_area']
        if 'rooms' in data:
            product.rooms = data['rooms']
        if 'sort_order' in data:
            product.sort_order = data['sort_order']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        if 'cover_image' in data or 'banner_images' in data:
            ProductImage.query.filter_by(product_id=product_id, image_type='banner').delete()
            
            cover_image = data.get('cover_image')
            banner_images = data.get('banner_images', [])
            
            if cover_image:
                banner_images = [cover_image] + banner_images
            
            for i, img in enumerate(banner_images):
                image_url = img.image_url if hasattr(img, 'image_url') else img
                if image_url:
                    db.session.add(ProductImage(
                        product_id=product.id,
                        image_url=image_url,
                        image_type='banner',
                        sort_order=i
                    ))
        
        if 'tags' in data:
            ProductTag.query.filter_by(product_id=product_id).delete()
            for tag_id in data['tags']:
                db.session.add(ProductTag(product_id=product.id, tag_id=tag_id))
        
        db.session.commit()
        return product.to_dict(include_images=True, include_tags=True)
    
    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False
        ProductImage.query.filter_by(product_id=product_id).delete()
        ProductTag.query.filter_by(product_id=product_id).delete()
        db.session.delete(product)
        db.session.commit()
        return True
    
    @staticmethod
    def increment_view_count(product_id):
        product = Product.query.get(product_id)
        if product:
            product.view_count += 1
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_product_list_raw(keyword=None, category_id=None, status=None, page=1, per_page=10):
        """管理后台产品列表查询（支持状态筛选）"""
        query = Product.query
        
        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if keyword:
            query = query.filter(
                (Product.title.like(f'%{keyword}%')) |
                (Product.model_number.like(f'%{keyword}%'))
            )
        
        query = query.order_by(Product.sort_order.desc(), Product.created_at.desc())
        items, total, page, per_page = paginate(query, page, per_page)
        
        products = []
        for item in items:
            product_dict = item.to_dict(include_images=True, include_tags=True)
            products.append(product_dict)
        
        return paginated(products, page, per_page, total)