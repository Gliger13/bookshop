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
product_list_schema = ProductSchema(many=True)


class ProductService:
    """Product Service

    Provides service methods that support CRUD operations for product resource
    """

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all product resources

        :return: list of all products
        """
        all_product_data = ProductDAO.get_all()
        return product_list_schema.dump(all_product_data), codes.ok

    @staticmethod
    def get(product_id: int) -> tuple[dict, int]:
        """Get product resource by its ID

        :param product_id: ID of the product to get
        :raise HTTPError: if product with the given ID does not exist
        :return: attributes of the product with given ID
        """
        product_data = ProductDAO.get_by_id(product_id)
        return product_schema.dump(product_data), codes.ok

    @staticmethod
    def create() -> tuple[dict | Response, int]:
        """Create product resource

        Validate and load create product request json using product schema.
        Create product model using Data Access Object.

        :raise HTTPException: raise if:
          - there are validation errors with create product request json
        :return: tuple of response json and status code
        """
        try:
            create_product_json = request.get_json()
            product_data = product_schema.load(create_product_json)
            ProductDAO.create(product_data)
            return product_schema.dump(product_data), codes.created
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def delete(product_id: int) -> tuple[dict[str, str], int]:
        """Delete product resource

        :param product_id: ID of the product to delete
        :raise HTTPException: if product with the given ID does not exist
        :return: tuple of response json and status code
        """
        ProductDAO.get_by_id(product_id)
        ProductDAO.delete(product_id)
        return {"message": "Product deleted successfully"}, codes.ok

    @staticmethod
    def update(product_id: int) -> tuple[dict | Response, int]:
        """Update product resource

        Check if the product with the given ID exists. Merge old product data
        with new data from the update product request json. Validate and load
        merged data. Update product model using Data Access Object.

        :raise HTTPException: raise if:
          - product with given ID does not exist
          - there are validation errors with merged product data
        :return: tuple of response json and status code
        """
        try:
            product_model = ProductDAO.get_by_id(product_id)
            product_data = product_schema.dump(product_model)
            update_product_request_json = request.get_json()
            product_data.update(update_product_request_json)
            updated_product_data = product_schema.load(product_data)
            ProductDAO.update(updated_product_data)
            return product_schema.dump(updated_product_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request
