"""Store item service

Module contains Store Item Service that provides methods with CRUD operations
for store item resources.
"""

from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.store_item import StoreItemDAO
from bookshop_app.schemas.store_item import StoreItemSchema

store_item_schema = StoreItemSchema()


class StoreItemService:
    """Store Item Service

    Provides service methods that support CRUD operations for store item
    resources
    """

    @staticmethod
    def get(store_item_id: int) -> dict:
        """Get store resource by id"""
        store_item_data = StoreItemDAO.get_by_id(store_item_id)
        return store_item_schema.dump(store_item_data)

    @staticmethod
    def get_all() -> list[dict]:
        """Get all store item resources"""
        all_store_item_data = StoreItemDAO.get_all()
        return store_item_schema.dump(all_store_item_data)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create store item resource"""
        create_store_item_json = request.get_json()
        store_item_data = store_item_schema.load(create_store_item_json)
        StoreItemDAO.create(store_item_data)
        return store_item_schema.dump(store_item_data), codes.created

    @staticmethod
    def delete(store_item_id: int) -> tuple[dict[str, str], int]:
        """Delete store item resource"""
        StoreItemDAO.get_by_id(store_item_id)
        StoreItemDAO.delete(store_item_id)
        return {"message": "Store deleted successfully"}, codes.ok

    @staticmethod
    def update(store_item_id: int) -> Response | tuple[dict, int]:
        """Update store item resource"""
        try:
            store_model = StoreItemDAO.get_by_id(store_item_id)
            store_item_data = store_item_schema.dump(store_model)
            update_store_request_json = request.get_json()
            store_item_data.update(update_store_request_json)
            updated_store_item_data = store_item_schema.load(store_item_data)
            StoreItemDAO.update(updated_store_item_data)
            return store_item_schema.dump(updated_store_item_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request, title="Bad Request", type="about:blank")
