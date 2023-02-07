"""Store Item controller"""
from flask import Response

from bookshop_app.authenticator import auth
from bookshop_app.services.store_item import StoreItemService


class StoreItemController:
    """Controller for Store Item"""

    @staticmethod
    @auth.login_required
    def get_all() -> list[dict]:
        """Get all store item resources"""
        return StoreItemService.get_all()

    @staticmethod
    @auth.login_required
    def get(store_item_id: int) -> dict:
        """Get store item resource by store item id"""
        return StoreItemService.get(store_item_id)

    @staticmethod
    @auth.login_required
    def create() -> Response | tuple[dict, int]:
        """Create store item resource"""
        return StoreItemService.create()

    @staticmethod
    @auth.login_required
    def delete(store_item_id: int) -> tuple[dict[str, str], int]:
        """Delete store item resource"""
        return StoreItemService.delete(store_item_id)

    @staticmethod
    @auth.login_required
    def update(store_item_id: int) -> Response | tuple[dict, int]:
        """Update store item resource"""
        return StoreItemService.update(store_item_id)
