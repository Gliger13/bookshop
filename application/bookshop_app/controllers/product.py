"""Product controller"""
from flask import Response

from bookshop_app.authenticator import auth
from bookshop_app.models.role import UserRole
from bookshop_app.services.product import ProductService


class ProductController:
    """Controller for Product"""

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all product resources"""
        return ProductService.get_all()

    @staticmethod
    def get(product_id: int) -> tuple[dict, int]:
        """Get product resource by product id"""
        return ProductService.get(product_id)

    @staticmethod
    @auth.login_required(role=[UserRole.ADMIN.value, UserRole.MANAGER.value])
    def create() -> Response | tuple[dict, int]:
        """Create product resource"""
        return ProductService.create()

    @staticmethod
    @auth.login_required(role=[UserRole.ADMIN.value, UserRole.MANAGER.value])
    def delete(product_id: int) -> tuple[dict, int]:
        """Delete product resource"""
        return ProductService.delete(product_id)

    @staticmethod
    @auth.login_required(role=[UserRole.ADMIN.value, UserRole.MANAGER.value])
    def update(product_id: int) -> tuple[Response | dict, int]:
        """Update product resource"""
        return ProductService.update(product_id)
