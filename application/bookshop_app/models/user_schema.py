"""
ORM Schemas
"""

from bookshop_app.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.user_model import User


class UserSchema(ma.SQLAlchemySchema):
    """User schema"""

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    login = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
