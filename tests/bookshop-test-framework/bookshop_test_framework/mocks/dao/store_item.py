"""Fake store_item data access object"""
from typing import Optional

from bookshop_app.models.store_item import StoreItemModel
from bookshop_app.schemas.store_item import StoreItemSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

store_item_schema = StoreItemSchema()


class FakeStoreItemDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[StoreItemModel] = []

    @classmethod
    def create(cls, store_item: StoreItemModel) -> None:
        """Create store item"""
        cls._data.append(store_item)

    @classmethod
    def get_by_id(cls, store_item_id: int) -> Optional[StoreItemModel]:
        """Get store item by id"""
        for store_item in cls._data:
            if store_item.id == store_item_id:
                return store_item
        return None

    @classmethod
    def get_all(cls) -> list[StoreItemModel]:
        """Return all store items"""
        return cls._data

    @classmethod
    def delete(cls, store_item_id: int) -> None:
        """Delete store item"""
        cls._data = [store_item for store_item in cls._data if store_item.id != store_item_id]

    @classmethod
    def update(cls, updated_store_item: StoreItemModel) -> None:
        """Update store item"""
        for store_item in cls._data:
            if store_item.id == updated_store_item.id:
                cls.delete(store_item.id)
                cls.create(updated_store_item)
                break
