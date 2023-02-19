"""Product service

Module contains Product Service that provides methods with CRUD operations for
product resource.
"""
from typing import Optional

from flask import abort, jsonify, request, Request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from bookshop_app.data_access_objects.product import ProductDAO
from bookshop_app.models.file import FileManagerFactory, FileValidator
from bookshop_app.models.product import ProductModel
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
        Create product model using Data Access Object. If request contains
        image then validate and save it using file manager.

        :raise HTTPException: raise if:
          - 415 - given request media type is not supported
          - 400 - there are validation errors with create product request json
        :return: tuple of response json and status code
        """
        try:
            create_product_attributes = ProductService.get_create_or_update_attributes_from_request(request)
            product_data = product_schema.load(create_product_attributes)
            ProductService.update_product_with_image(product_data, request.files)
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
        merged data. If request contains image then validate and save it using
        file manager, delete old attached image if it exists. Update product
        model using Data Access Object.

        :raise HTTPException: raise if:
          - 415 - given request media type is not supported
          - 404 - product with given ID does not exist
          - 400 - there are validation errors with merged product data
        :return: tuple of response json and status code
        """
        try:
            update_product_attributes = ProductService.get_create_or_update_attributes_from_request(request)
            product_model = ProductDAO.get_by_id(product_id)
            product_data = product_schema.dump(product_model)
            product_data.update(update_product_attributes)
            updated_product_data = product_schema.load(product_data)

            ProductService.update_product_with_image(updated_product_data, request.files)
            ProductDAO.update(updated_product_data)
            return product_schema.dump(updated_product_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def update_product_with_image(product_to_set_image: ProductModel, request_files: dict) -> None:
        """Update given product with the image from request files

        Get image from request files and validate it. Save image file using
        file manager. Update the given product model with the saved image path.
        If the product model already has an image path, delete the old saved
        image.

        :param product_to_set_image: product model to set image from files
        :param request_files: files attributes from the request
        :raise HTTPException: raise if
          - request files do not have image with image mimetype
          - there are verification errors with the image from the request files
        """
        image_to_save: FileStorage = request_files.get("image")
        if not image_to_save:
            return None

        if "image" not in image_to_save.mimetype:
            abort(codes.unsupported_media_type, "Unsupported media type. Given file is not image")

        image_binary = image_to_save.read()
        FileValidator.validate_image(image_to_save)

        file_manager = FileManagerFactory.get_by_environment_config()
        saved_image_path = file_manager.save(image_to_save.filename, image_binary)

        if product_to_set_image.image_path:
            file_manager.delete(product_to_set_image.image_path)

        product_to_set_image.image_path = saved_image_path
        return None

    @staticmethod
    def get_create_or_update_attributes_from_request(create_or_update_request: Request) -> Optional[dict]:
        """Get create or update product attributes from the request

        :param create_or_update_request: request to create or update product
        :return: attributes of product to create or update or None if can not
            get attributes from request
        """
        if request.is_json:
            return create_or_update_request.get_json()
        if request.mimetype == "multipart/form-data":
            create_or_update_product_attributes = create_or_update_request.form.to_dict()
            create_or_update_product_attributes.pop("image", None)
            return create_or_update_product_attributes
        abort(codes.unsupported_media_type, "Unsupported Media Type")
