"""ORM Store Item Model"""
from bookshop_app.database.database import db
from bookshop_app.models.product import ProductModel


class StoreItemModel(db.Model):
    """Store Item model"""

    __tablename__ = "store_items"
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey(f"{ProductModel.__tablename__}.id"))
    product = db.relationship(ProductModel.__name__)

    available_quantity = db.Column(db.Integer, default=0)
    booked_quantity = db.Column(db.Integer, default=0)
    sold_quantity = db.Column(db.Integer, default=0)
