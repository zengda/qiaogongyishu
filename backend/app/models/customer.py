from app.extensions import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    wechat = db.Column(db.String(100))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    building_area_budget = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_title = db.Column(db.String(200))
    source = db.Column(db.String(50), default='小程序')
    status = db.Column(db.Enum('new', 'contacted', 'followed', 'closed'), default='new')
    remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'wechat': self.wechat,
            'province': self.province,
            'city': self.city,
            'building_area_budget': self.building_area_budget,
            'product_id': self.product_id,
            'product_title': self.product_title,
            'source': self.source,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }