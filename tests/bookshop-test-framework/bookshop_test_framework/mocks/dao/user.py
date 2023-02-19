"""Fake User data access object"""
from typing import Optional

from bookshop_app.models.user import UserModel
from bookshop_app.schemas.user import UserSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

user_schema = UserSchema()


class FakeUserDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[UserModel] = []

    @classmethod
    def create(cls, user: UserModel) -> None:
        """Create user"""
        cls._data.append(user)

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[UserModel]:
        """Get user by id"""
        for user in cls._data:
            if user.id == user_id:
                return user
        return None

    @classmethod
    def get_by_login(cls, user_login: str) -> Optional[UserModel]:
        """Get user by login"""
        for user in cls._data:
            if user.login == user_login:
                return user
        return None

    @classmethod
    def get_all(cls) -> list[UserModel]:
        """Return all users"""
        return cls._data

    @classmethod
    def delete(cls, user_id: int) -> None:
        """Delete user"""
        cls._data = [user for user in cls._data if user.id != user_id]

    @classmethod
    def update(cls, updated_user_model: UserModel) -> None:
        """Update user"""
        for user in cls._data:
            user_id = updated_user_model.id
            if user.id == user_id:
                cls.delete(user_id)
                cls.create(updated_user_model)
                break
