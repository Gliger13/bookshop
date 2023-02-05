"""Product service

Module contains Product Service that provides methods with CRUD operations for
product resource.
"""

from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.product import ProductDAO
from bookshop_app.schemas.product import ProductSchema

product_schema = ProductSchema()


class ProductService:
    """Product Service

    Provides service methods that support CRUD operations for product resource
    """

    @staticmethod
    def get(product_id: int) -> dict:
        """Get product resource by id"""
        product_data = ProductDAO.get_by_id(product_id)
        return product_schema.dump(product_data)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create product resource"""
        create_product_json = request.get_json()
        product_data = product_schema.load(create_product_json)
        ProductDAO.create(product_data)
        return product_schema.dump(product_data), codes.created

    @staticmethod
    def delete(product_id: int) -> tuple[dict[str, str], int]:
        """Delete product resource"""
        ProductDAO.get_by_id(product_id)
        ProductDAO.delete(product_id)
        return {'message': 'Product deleted successfully'}, codes.ok

    @staticmethod
    def update(product_id: int) -> Response | tuple[dict, int]:
        """Update product resource"""
        try:
            product_model = ProductDAO.get_by_id(product_id)
            product_data = product_schema.dump(product_model)
            update_product_request_json = request.get_json()
            product_data.update(update_product_request_json)
            updated_product_data = product_schema.load(product_data)
            ProductDAO.update(updated_product_data)
            return product_schema.dump(updated_product_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request, title="Bad Request", type="about:blank")
