"""Store service

Module contains Store Service that provides methods with CRUD operations for
store resource.
"""

from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.store import StoreDAO
from bookshop_app.schemas.store import StoreSchema

store_schema = StoreSchema()


class StoreService:
    """Product Service

    Provides service methods that support CRUD operations for store resource
    """

    @staticmethod
    def get(store_id: int) -> dict:
        """Get store resource by id"""
        store_data = StoreDAO.get_by_id(store_id)
        return store_schema.dump(store_data)

    @staticmethod
    def get_all() -> list[dict]:
        """Get all store item resources"""
        all_store_data = StoreDAO.get_all()
        return store_schema.dump(all_store_data)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create store resource"""
        create_store_json = request.get_json()
        store_data = store_schema.load(create_store_json)
        StoreDAO.create(store_data)
        return store_schema.dump(store_data), codes.created

    @staticmethod
    def delete(store_id: int) -> tuple[dict[str, str], int]:
        """Delete store resource"""
        StoreDAO.get_by_id(store_id)
        StoreDAO.delete(store_id)
        return {"message": "Store deleted successfully"}, codes.ok

    @staticmethod
    def update(store_id: int) -> Response | tuple[dict, int]:
        """Update store resource"""
        try:
            store_model = StoreDAO.get_by_id(store_id)
            store_data = store_schema.dump(store_model)
            update_store_request_json = request.get_json()
            store_data.update(update_store_request_json)
            updated_store_data = store_schema.load(store_data)
            StoreDAO.update(updated_store_data)
            return store_schema.dump(updated_store_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request, title="Bad Request", type="about:blank")
