"""Store controller"""
from flask import Response

from bookshop_app.authenticator import auth
from bookshop_app.services.store import StoreService


class StoreController:
    """Controller for Store"""

    @staticmethod
    @auth.login_required
    def get(store_id: int) -> dict:
        """Get store resource by store id"""
        return StoreService.get(store_id)

    @staticmethod
    @auth.login_required
    def create() -> Response | tuple[dict, int]:
        """Create store resource"""
        return StoreService.create()

    @staticmethod
    @auth.login_required
    def delete(store_id: int) -> tuple[dict[str, str], int]:
        """Delete store resource"""
        return StoreService.delete(store_id)

    @staticmethod
    @auth.login_required
    def update(store_id: int) -> Response | tuple[dict, int]:
        """Update store resource"""
        return StoreService.update(store_id)
