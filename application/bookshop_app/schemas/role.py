"""Role schema"""
from marshmallow import EXCLUDE

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.role import RoleModel
from bookshop_app.models.role import UserRole


class RoleSchema(ma.SQLAlchemySchema):
    """Role schema"""

    class Meta:
        """Configure Schema behavior"""

        model = RoleModel
        load_instance = True
        sqla_session = db.session
        unknown = EXCLUDE

    id = ma.auto_field()
    name = ma.Enum(UserRole)
