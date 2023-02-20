"""Store Item Data Access Object"""
from typing import Final

from bookshop_app.database.database import db
from bookshop_app.models.store_item import StoreItemModel

STORE_NOT_FOUND: Final = "Store item not found for id: {store_item_id}"


class StoreItemDAO:
    """Data Access Object class for Store Item Model"""

    @staticmethod
    def create(store_item: StoreItemModel) -> None:
        """Create store item in database"""
        db.session.add(store_item)
        db.session.commit()

    @staticmethod
    def get_all() -> list[StoreItemModel]:
        """Return all store items from database"""
        return db.session.query(StoreItemModel).all()

    @staticmethod
    def get_by_id(store_item_id: int) -> StoreItemModel:
        """Get store item by id from database"""
        return db.session.query(StoreItemModel).get_or_404(
            store_item_id,
            description=STORE_NOT_FOUND.format(store_item_id=store_item_id))

    @staticmethod
    def update(updated_store_item: StoreItemModel) -> None:
        """Update store item in database"""
        db.session.merge(updated_store_item)
        db.session.commit()

    @staticmethod
    def delete(store_item_id: int) -> None:
        """Delete store item from database"""
        item = db.session.query(StoreItemModel).filter_by(id=store_item_id).first()
        db.session.delete(item)
        db.session.commit()
