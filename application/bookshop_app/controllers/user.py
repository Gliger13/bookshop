"""User controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import multi_auth
from bookshop_app.services.authentication import required_same_user_id_or_roles
from bookshop_app.services.user import UserService


class UserController:
    """Controller for User"""

    @staticmethod
    @multi_auth.login_required
    def get_all() -> tuple[list[dict], int]:
        """Get all user resources."""
        return UserService.get_all()

    @staticmethod
    @multi_auth.login_required
    @required_same_user_id_or_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def get(user_id: int) -> tuple[dict, int]:
        """Get user resource by user id"""
        return UserService.get(user_id)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create user resource"""
        return UserService.create()

    @staticmethod
    @multi_auth.login_required
    @required_same_user_id_or_roles(roles=[UserRole.ADMIN])
    def delete(user_id: int) -> tuple[dict, int]:
        """Delete user resource"""
        return UserService.delete(user_id)

    @staticmethod
    @multi_auth.login_required
    @required_same_user_id_or_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def update(user_id: int) -> tuple[Response | dict, int]:
        """Update user resource"""
        return UserService.update(user_id)
