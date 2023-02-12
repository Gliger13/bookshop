"""Store item service

Module contains Store Item Service that provides methods with CRUD operations
for store item resources.
"""
from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.product import ProductDAO
from bookshop_app.data_access_objects.store_item import StoreItemDAO
from bookshop_app.schemas.store_item import StoreItemSchema

store_item_schema = StoreItemSchema()
store_item_list_schema = StoreItemSchema(many=True)


class StoreItemService:
    """Store Item Service

    Provides service methods that support CRUD operations for store item
    resources
    """

    @staticmethod
    def get(store_item_id: int) -> tuple[dict, int]:
        """Get store resource by its ID

        :param store_item_id: ID of the store item to get
        :raise HTTPException: if store item with the given ID does not exist
        :return: tuple of response json and status code
        """
        store_item_data = StoreItemDAO.get_by_id(store_item_id)
        return store_item_schema.dump(store_item_data), codes.ok

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all store item resources

        :return: tuple of response json and status code
        """
        all_store_item_data = StoreItemDAO.get_all()
        return store_item_list_schema.dump(all_store_item_data), codes.ok

    @staticmethod
    def create() -> tuple[Response | dict, int]:
        """Create store item resource

        Validate and load create store item request json using store item
        schema. Check if store item with the given ID exists. Create store item
        model using Data Access Object.

        :raise HTTPException: raise if:
          - there are validation errors with create store item request json
          - store item with the given ID does not exist
        :return: tuple of response json and status code
        """
        try:
            create_store_item_json = request.get_json()
            store_item_data = store_item_schema.load(create_store_item_json)
            ProductDAO.get_by_id(create_store_item_json["product_id"])
            StoreItemDAO.create(store_item_data)
            return store_item_schema.dump(store_item_data), codes.created
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def delete(store_item_id: int) -> tuple[dict[str, str], int]:
        """Delete store item resource with the given ID

        :param store_item_id: ID of the store item to delete
        :raise HTTPException: raise if:
          - store item with the given ID does not exist
        :return: tuple of response json and status code
        """
        StoreItemDAO.get_by_id(store_item_id)
        StoreItemDAO.delete(store_item_id)
        return {"message": "Store deleted successfully"}, codes.ok

    @staticmethod
    def update(store_item_id: int) -> tuple[Response | dict, int]:
        """Update store item resource with the given ID

        Check if the store item with the given ID exists. Merge old store item
        data with the new data from the update store item request json.
        Validate and load merged data using store item schema. Update store
        item model using Data Access Object.

        :raise HTTPException: raise if:
          - store item with the given ID does not exist
          - there are validation errors with merged product data
          - product ID provided and the given ID does not exist
        :return: tuple of response json and status code
        """
        try:
            store_model = StoreItemDAO.get_by_id(store_item_id)
            store_item_data = store_item_schema.dump(store_model)
            update_store_request_json = request.get_json()
            store_item_data.update(update_store_request_json)
            updated_store_item_data = store_item_schema.load(store_item_data)
            if product_id_to_update := updated_store_item_data.get("product_id"):
                ProductDAO.get_by_id(product_id_to_update)
            StoreItemDAO.update(updated_store_item_data)
            return store_item_schema.dump(updated_store_item_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request
