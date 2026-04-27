from app.extensions import db

class ProductTag(db.Model):
    __tablename__ = 'product_tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    
    product = db.relationship('Product', back_populates='tags')
    tag = db.relationship('Tag', back_populates='products')
    
    __table_args__ = (
        db.UniqueConstraint('product_id', 'tag_id', name='unique_product_tag'),
    )