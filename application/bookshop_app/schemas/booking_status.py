"""Booking status schema"""
from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.booking_status import BookingStatusModel


class BookingStatusSchema(ma.SQLAlchemySchema):
    """Booking status schema"""

    class Meta:
        model = BookingStatusModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field()
