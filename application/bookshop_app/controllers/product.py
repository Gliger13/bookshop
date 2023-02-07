"""Product controller"""
from flask import Response

from bookshop_app.authenticator import auth
from bookshop_app.services.product import ProductService


class ProductController:
    """Controller for Product"""

    @staticmethod
    def get_all() -> list[dict]:
        """Get all product resources"""
        return ProductService.get_all()

    @staticmethod
    def get(product_id: int) -> dict:
        """Get product resource by product id"""
        return ProductService.get(product_id)

    @staticmethod
    @auth.login_required
    def create() -> Response | tuple[dict, int]:
        """Create product resource"""
        return ProductService.create()

    @staticmethod
    @auth.login_required
    def delete(product_id: int) -> tuple[dict[str, str], int]:
        """Delete product resource"""
        return ProductService.delete(product_id)

    @staticmethod
    @auth.login_required
    def update(product_id: int) -> Response | tuple[dict, int]:
        """Update product resource"""
        return ProductService.update(product_id)
