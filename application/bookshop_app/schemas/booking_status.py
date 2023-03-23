"""Booking status schema"""
from marshmallow import EXCLUDE

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.booking_status import BookingStatus
from bookshop_app.models.booking_status import BookingStatusModel


class BookingStatusSchema(ma.SQLAlchemySchema):
    """Booking status schema"""

    class Meta:
        """Configure Schema behavior"""

        model = BookingStatusModel
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE

    id = ma.auto_field()
    name = ma.Enum(BookingStatus)
