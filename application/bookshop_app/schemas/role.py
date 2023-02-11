"""Role schema"""
from bookshop_app.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.role import RoleModel


class RoleSchema(ma.SQLAlchemySchema):
    """Role schema"""

    class Meta:
        model = RoleModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field()
