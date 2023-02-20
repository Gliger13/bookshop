"""Roles Data Access Object"""
from typing import Final

from bookshop_app.database.database import db
from bookshop_app.models.role import RoleModel

ROLE_NOT_FOUND: Final = "Role not found with id: {role_id}"


class RoleDAO:
    """Data Access Object class for Role Model"""

    @staticmethod
    def get_all() -> list[RoleModel]:
        """Return all roles from database"""
        return db.session.query(RoleModel).all()

    @staticmethod
    def get_by_id(role_id: int) -> RoleModel:
        """Get role by id from database"""
        return db.session.query(RoleModel).get_or_404(
            role_id,
            description=ROLE_NOT_FOUND.format(role_id=role_id))
