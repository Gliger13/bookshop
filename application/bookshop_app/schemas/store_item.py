"""ORM Store Item Schema"""
from marshmallow import validates, ValidationError

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.store_item import StoreItemModel


class StoreItemSchema(ma.SQLAlchemySchema):
    """Store item schema"""

    class Meta:
        model = StoreItemModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    product_id = ma.auto_field()

    available_quantity = ma.auto_field()
    booked_quantity = ma.auto_field()
    sold_quantity = ma.auto_field()

    @validates("booked_quantity")
    def validate_booked_quantity(self, booked_quantity: int) -> None:
        """Validate booked product quantity

        :param booked_quantity: quantity of product that were booked to validate
        :raise ValidationError: if something wrong with the given quantity
        """
        if booked_quantity is not None and booked_quantity < 0:
            raise ValidationError("Product booked quantity must not be less than zero")

    @validates("sold_quantity")
    def validate_sold_quantity(self, sold_quantity: int) -> None:
        """Validate booked product quantity

        :param sold_quantity: quantity of product that were sold to validate
        :raise ValidationError: if something wrong with the given quantity
        """
        if sold_quantity is not None and sold_quantity < 0:
            raise ValidationError("Product sold quantity must not be less than zero")
