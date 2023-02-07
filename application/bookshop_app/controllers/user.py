"""User controller"""
from flask import Response

from bookshop_app.authenticator import auth
from bookshop_app.services.user import UserService


class UserController:
    """Controller for User"""

    @staticmethod
    @auth.login_required
    def get_all() -> list[dict]:
        """Get all user resources"""
        return UserService.get_all()

    @staticmethod
    @auth.login_required
    def get(user_id: int) -> dict:
        """Get user resource by user id"""
        return UserService.get(user_id)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create user resource"""
        return UserService.create()

    @staticmethod
    @auth.login_required
    def delete(user_id: int) -> tuple[dict[str, str], int]:
        """Delete user resource"""
        return UserService.delete(user_id)

    @staticmethod
    @auth.login_required
    def update(user_id: int) -> Response | tuple[dict, int]:
        """Update user resource"""
        return UserService.update(user_id)
