"""ORM Store Item Model"""
from bookshop_app.database import db


class StoreItemModel(db.Model):
    """Store Item model"""

    id = db.Column(db.Integer, primary_key=True)

    product = db.relationship('ProductModel', backref='store', lazy=True)

    available_quantity = db.Column(db.Integer)
    booked_quantity = db.Column(db.Integer)
    sold_quantity = db.Column(db.Integer)
