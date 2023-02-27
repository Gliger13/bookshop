"""Store Item controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import auth
from bookshop_app.services.store_item import StoreItemService


class StoreItemController:
    """Controller for Store Item"""

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all store item resources"""
        return StoreItemService.get_all()

    @staticmethod
    def get(store_item_id: int) -> tuple[dict, int]:
        """Get store item resource by store item id"""
        return StoreItemService.get(store_item_id)

    @staticmethod
    def create() -> tuple[Response | dict, int]:
        """Create store item resource"""
        return StoreItemService.create()

    @staticmethod
    def delete(store_item_id: int) -> tuple[dict, int]:
        """Delete store item resource"""
        return StoreItemService.delete(store_item_id)

    @staticmethod
    def update(store_item_id: int) -> tuple[Response | dict, int]:
        """Update store item resource"""
        return StoreItemService.update(store_item_id)
