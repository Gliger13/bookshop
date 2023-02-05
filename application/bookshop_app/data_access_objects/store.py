"""Store Data Access Object"""

from bookshop_app.database import db
from bookshop_app.models.store import StoreModel


class StoreMessages:
    """Store messages and templates"""

    STORE_NOT_FOUND = "Store not found for id: {store_id}"


class StoreDAO:
    """Data Access Object class for Store Model"""

    @staticmethod
    def create(store: StoreModel) -> None:
        """Create store in database"""
        db.session.add(store)
        db.session.commit()

    @staticmethod
    def get_by_id(store_id: int) -> StoreModel:
        """Get store by id from database"""
        return db.session.query(StoreModel).get_or_404(
            store_id,
            description=StoreMessages.STORE_NOT_FOUND.format(store_id=store_id))

    @staticmethod
    def update(store_data: dict) -> None:
        """Update store in database"""
        db.session.merge(store_data)
        db.session.commit()

    @staticmethod
    def delete(store_id: int) -> None:
        """Delete store from database"""
        item = db.session.query(StoreModel).filter_by(id=store_id).first()
        db.session.delete(item)
        db.session.commit()
