"""ORM Booking model"""

from bookshop_app.database import db
from bookshop_app.models.booking_status import BookingStatusModel
from bookshop_app.models.product import ProductModel
from bookshop_app.models.user import UserModel


class BookingModel(db.Model):
    """Booking model"""

    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship(ProductModel.__name__)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(UserModel.__name__)

    status_id = db.Column(db.Integer, db.ForeignKey("booking_statuses.id"))
    status = db.relationship(BookingStatusModel.__name__)

    delivery_address = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    date = db.Column(db.Date)
    time = db.Column(db.DateTime)
