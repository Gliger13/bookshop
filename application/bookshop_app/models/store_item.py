"""ORM Store Item Model"""
from bookshop_app.database.database import db
from bookshop_app.models.product import ProductModel


class StoreItemModel(db.Model):
    """Store Item model"""

    __tablename__ = "store_items"
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship(ProductModel.__name__)

    available_quantity = db.Column(db.Integer)
    booked_quantity = db.Column(db.Integer)
    sold_quantity = db.Column(db.Integer)
