"""ORM Store Schema"""
from bookshop_app.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.store import StoreModel


class StoreSchema(ma.SQLAlchemySchema):
    """Store schema"""

    class Meta:
        model = StoreModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()

    product = ma.auto_field()

    available_quantity = ma.auto_field()
    booked_quantity = ma.auto_field()
    sold_quantity = ma.auto_field()
