"""ORM Product schema"""
from marshmallow import EXCLUDE, validate, validates, ValidationError

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.product import ProductModel


class ProductSchema(ma.SQLAlchemySchema):
    """Product schema"""

    class Meta:
        """Configure Schema behavior"""

        model = ProductModel
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE

    id = ma.auto_field()

    name = ma.auto_field()
    description = ma.auto_field()
    author = ma.auto_field()
    price = ma.auto_field()
    image_path = ma.auto_field()

    @validates("name")
    def validate_name(self, name: str) -> None:
        """Validate product name

        :param name: name of the product to validate
        :raise ValidationError: if something wrong with the given name
        """
        if name:
            validate.Length(min=2, max=256)(name)

    @validates("author")
    def validate_author(self, author: str) -> None:
        """Validate product author

        :param author: name of the author to validate
        :raise ValidationError: if something wrong with the given author
        """
        if author:
            validate.Length(min=2, max=256)(author)

    @validates("price")
    def validate_price(self, price: float) -> None:
        """Validate product price

        :param price: price of the product to validate
        :raise ValidationError: if something wrong with the given price
        """
        if price is not None and price < 0:
            raise ValidationError("Product price must not be less than zero")
