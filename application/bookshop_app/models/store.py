"""ORM Store Model"""
from bookshop_app.database import db


class StoreModel(db.Model):
    """Store model"""

    id = db.Column(db.Integer, primary_key=True)

    product = db.relationship('Product', backref='store', lazy=True)

    available_quantity = db.Column(db.Integer)
    booked_quantity = db.Column(db.Integer)
    sold_quantity = db.Column(db.Integer)
