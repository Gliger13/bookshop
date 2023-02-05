"""Controller module."""

from bookshop_app.authenticator import auth
from bookshop_app.services.user import UserService


class UserController:

    @staticmethod
    def get(user_id: int):
        """Get user resource."""
        return UserService.get(user_id)

    @staticmethod
    @auth.login_required
    def get_all():
        """Get all user resources."""
        return UserService.get_all()

    @staticmethod
    def create():
        """Create user resource."""
        return UserService.create()

    @staticmethod
    def delete(user_id: int):
        """Delete user resource"""
        return UserService.delete(user_id)

    @staticmethod
    def update(user_id: int):
        """Update user resource"""
        return UserService.update(user_id)
