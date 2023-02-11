"""ORM Product schema"""

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.product import ProductModel


class ProductSchema(ma.SQLAlchemySchema):
    """Product schema"""

    class Meta:
        model = ProductModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    name = ma.auto_field()
    description = ma.auto_field()
    author = ma.auto_field()
    price = ma.auto_field()
    image_path = ma.auto_field()
