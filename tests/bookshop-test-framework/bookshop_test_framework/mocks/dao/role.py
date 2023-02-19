"""Fake role data access object"""
from typing import Optional

from bookshop_app.models.role import RoleModel, UserRole
from bookshop_app.schemas.role import RoleSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

role_schema = RoleSchema()


class FakeRoleDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[RoleModel] = [
        *[RoleModel(id=index + 1, name=role) for index, role in enumerate(UserRole)]
    ]

    @classmethod
    def get_by_id(cls, role_id: int) -> Optional[RoleModel]:
        """Get role by id"""
        for role in cls._data:
            if role.id == role_id:
                return role
        return None

    @classmethod
    def get_all(cls) -> list[RoleModel]:
        """Return all roles"""
        return cls._data
