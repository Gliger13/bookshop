"""Fake product data access object"""
from typing import Optional

from bookshop_app.models.product import ProductModel
from bookshop_app.schemas.product import ProductSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

product_schema = ProductSchema()


class FakeProductDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[ProductModel] = []

    @classmethod
    def create(cls, product: ProductModel) -> None:
        """Create product"""
        cls._data.append(product)

    @classmethod
    def get_by_id(cls, product_id: int) -> Optional[ProductModel]:
        """Get product by id"""
        for product in cls._data:
            if product.id == product_id:
                return product
        return None

    @classmethod
    def get_all(cls) -> list[ProductModel]:
        """Return all products"""
        return cls._data

    @classmethod
    def delete(cls, product_id: int) -> None:
        """Delete product"""
        cls._data = [product for product in cls._data if product.id != product_id]

    @classmethod
    def update(cls, updated_product_model: ProductModel) -> None:
        """Update product"""
        for product in cls._data:
            if product.id == updated_product_model.id:
                cls.delete(product.id)
                cls.create(updated_product_model)
                break
