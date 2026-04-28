from app.extensions import db
from datetime import datetime
from flask import current_app

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    model_number = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.Text)
    floor_area = db.Column(db.String(50))
    building_area = db.Column(db.String(50))
    rooms = db.Column(db.String(50))
    sort_order = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    category = db.relationship('Category', back_populates='products')
    images = db.relationship('ProductImage', back_populates='product', order_by='ProductImage.sort_order')
    tags = db.relationship('ProductTag', back_populates='product')
    
    def to_dict(self, include_images=False, include_tags=False):
        result = {
            'id': self.id,
            'title': self.title,
            'model_number': self.model_number,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'description': self.description,
            'floor_area': self.floor_area,
            'building_area': self.building_area,
            'rooms': self.rooms,
            'sort_order': self.sort_order,
            'view_count': self.view_count,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if include_images:
            banner_images = [img.to_dict() for img in self.images if img.image_type == 'banner']
            detail_images = [img.to_dict() for img in self.images if img.image_type == 'detail']
            result['banner_images'] = banner_images
            result['detail_images'] = detail_images
            result['cover_image'] = banner_images[0]['image_url'] if banner_images else None
        else:
            banner_images = [img for img in self.images if img.image_type == 'banner']
            if banner_images:
                image_url = banner_images[0].image_url
                if image_url and not image_url.startswith('http'):
                    if image_url.startswith('/uploads/'):
                        image_url = current_app.config['LOCAL_BASE_URL'].replace('/uploads', '') + image_url
                    else:
                        image_url = current_app.config['LOCAL_BASE_URL'] + '/' + image_url
                result['cover_image'] = image_url
            else:
                result['cover_image'] = None
        
        if include_tags:
            result['tags'] = [pt.tag.to_dict() for pt in self.tags]
        
        return result