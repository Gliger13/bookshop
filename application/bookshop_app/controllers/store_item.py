"""Store Item controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import multi_auth
from bookshop_app.services.store_item import StoreItemService


class StoreItemController:
    """Controller for Store Item"""

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def get_all() -> tuple[list[dict], int]:
        """Get all store item resources"""
        return StoreItemService.get_all()

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def get(store_item_id: int) -> tuple[dict, int]:
        """Get store item resource by store item id"""
        return StoreItemService.get(store_item_id)

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def create() -> tuple[Response | dict, int]:
        """Create store item resource"""
        return StoreItemService.create()

    @staticmethod
    @multi_auth.login_required(role=[UserRole.ADMIN])
    def delete(store_item_id: int) -> tuple[dict, int]:
        """Delete store item resource"""
        return StoreItemService.delete(store_item_id)

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def update(store_item_id: int) -> tuple[Response | dict, int]:
        """Update store item resource"""
        return StoreItemService.update(store_item_id)
