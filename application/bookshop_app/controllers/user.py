"""User controller"""
from flask import Response

from bookshop_app.services.authentication import auth
from bookshop_app.services.user import UserService


class UserController:
    """Controller for User"""

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all user resources"""
        return UserService.get_all()

    @staticmethod
    def get(user_id: int) -> tuple[dict, int]:
        """Get user resource by user id"""
        return UserService.get(user_id)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create user resource"""
        return UserService.create()

    @staticmethod
    def delete(user_id: int) -> tuple[dict, int]:
        """Delete user resource"""
        return UserService.delete(user_id)

    @staticmethod
    @auth.login_required
    def update(user_id: int) -> tuple[Response | dict, int]:
        """Update user resource"""
        return UserService.update(user_id)
