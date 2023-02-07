"""ORM Booking model"""

from enum import Enum

from bookshop_app.database import db


class BookingStatus(Enum):
    """Booking statuses"""

    SUBMITTED = "Submitted"
    REJECTED = "Rejected"
    APPROVED = "Approved"
    CANCELED = "Canceled"
    IN_DELIVERY = "In delivery"
    COMPLETED = "Completed"


class BookingModel(db.Model):
    """Booking model"""

    id = db.Column(db.Integer, primary_key=True)

    product = db.relationship('ProductModel', backref='product', lazy=True)
    user = db.relationship('UserModel', backref='booking', lazy=True)

    delivery_address = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    date = db.Column(db.String(256))
    time = db.Column(db.String(256))

    status = db.Column(db.String(256))
