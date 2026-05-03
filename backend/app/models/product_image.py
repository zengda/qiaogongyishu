from app.extensions import db
from datetime import datetime
from app.utils.image_url import fix_image_url

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    image_url = db.Column(db.String(500), nullable=False)
    image_type = db.Column(db.Enum('banner', 'detail'), default='banner')
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    product = db.relationship('Product', back_populates='images')
    
    def to_dict(self):
        image_url = fix_image_url(self.image_url)
        
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_url': image_url,
            'image_type': self.image_type,
            'sort_order': self.sort_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }