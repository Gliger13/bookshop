"""ORM User Schemas"""

from bookshop_app.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    """User schema"""

    class Meta:
        model = UserModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    login = ma.auto_field()

    role_id = ma.auto_field()

    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    address = ma.auto_field()
