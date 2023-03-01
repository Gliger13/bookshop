"""Product controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import multi_auth
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
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def create() -> Response | tuple[dict, int]:
        """Create product resource"""
        return ProductService.create()

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def delete(product_id: int) -> tuple[dict, int]:
        """Delete product resource"""
        return ProductService.delete(product_id)

    @staticmethod
    @multi_auth.login_required(role=[UserRole.MANAGER, UserRole.ADMIN])
    def update(product_id: int) -> tuple[Response | dict, int]:
        """Update product resource"""
        return ProductService.update(product_id)
