"""Product Data Access Object"""
from typing import Final

from bookshop_app.database.database import db
from bookshop_app.models.product import ProductModel

PRODUCT_NOT_FOUND: Final = "Product not found for id: {product_id}"


class ProductDAO:
    """Data Access Object class for Product Model"""

    @staticmethod
    def create(product: ProductModel) -> None:
        """Create product in database"""
        db.session.add(product)
        db.session.commit()

    @staticmethod
    def get_all() -> list[ProductModel]:
        """Return all products from database"""
        return db.session.query(ProductModel).all()

    @staticmethod
    def get_by_id(product_id: int) -> ProductModel:
        """Get product by id from database"""
        return db.session.query(ProductModel).get_or_404(
            product_id, description=PRODUCT_NOT_FOUND.format(product_id=product_id)
        )

    @staticmethod
    def update(updated_product: ProductModel) -> None:
        """Update product in database"""
        db.session.merge(updated_product)
        db.session.commit()

    @staticmethod
    def delete(product_id: int) -> None:
        """Delete product from database"""
        item = db.session.query(ProductModel).filter_by(id=product_id).first()
        db.session.delete(item)
        db.session.commit()
