from app.extensions import db
from datetime import datetime
from flask import current_app

class Banner(db.Model):
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    image_url = db.Column(db.String(500), nullable=False)
    link_type = db.Column(db.Enum('none', 'product', 'category', 'url'), default='none')
    link_value = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def is_valid(self):
        now = datetime.now()
        if self.start_time and now < self.start_time:
            return False
        if self.end_time and now > self.end_time:
            return False
        return self.is_active
    
    def to_dict(self):
        image_url = self.image_url
        if image_url and not image_url.startswith('http'):
            if image_url.startswith('/uploads/'):
                image_url = current_app.config['LOCAL_BASE_URL'].replace('/uploads', '') + image_url
            else:
                image_url = current_app.config['LOCAL_BASE_URL'] + '/' + image_url
        
        return {
            'id': self.id,
            'title': self.title,
            'image_url': image_url,
            'link_type': self.link_type,
            'link_value': self.link_value,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }