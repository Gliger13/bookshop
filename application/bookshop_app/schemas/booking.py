"""ORM Booking schema"""

from bookshop_app.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.booking import BookingModel


class BookingSchema(ma.SQLAlchemySchema):
    """Booking schema"""

    class Meta:
        model = BookingModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    product = ma.auto_field()
    user = ma.auto_field()

    delivery_address = ma.auto_field()
    quantity = ma.auto_field()

    date = ma.auto_field()
    time = ma.auto_field()

    status = ma.auto_field()
