"""ORM Booking schema"""
from marshmallow import validates, ValidationError

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.booking import BookingModel


class BookingSchema(ma.SQLAlchemySchema):
    """Booking schema"""

    class Meta:
        """Configure Schema behavior"""

        model = BookingModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    product_id = ma.auto_field()
    user_id = ma.auto_field()
    status_id = ma.auto_field()

    delivery_address = ma.auto_field()
    quantity = ma.auto_field()

    delivery_date = ma.auto_field()
    delivery_time = ma.auto_field()

    @validates("quantity")
    def validate_quantity(self, quantity: int) -> None:
        """Validate product quantity

        Product quantity to book MUST be greater than 0.

        :param quantity: quantity of the product to validate
        :raise ValidationError: if something wrong with the given quantity
        """
        if quantity <= 0:
            raise ValidationError("Product quantity must not be less than zero")
