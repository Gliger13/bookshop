"""Roles Data Access Object"""
from bookshop_app.database import db
from bookshop_app.models.role import RoleModel


class RolesMessages:
    """Roles messages and templates"""

    ROLE_NOT_FOUND = "Role not found with id: {role_id}"


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
            description=RolesMessages.ROLE_NOT_FOUND.format(role_id=role_id))
