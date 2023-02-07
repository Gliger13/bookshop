"""Product Data Access Object"""

from bookshop_app.database import db
from bookshop_app.models.product import ProductModel


class ProductMessages:
    """Booking messages and templates"""

    PRODUCT_NOT_FOUND = "Product not found for id: {product_id}"


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
            product_id,
            description=ProductMessages.PRODUCT_NOT_FOUND.format(product_id=product_id))

    @staticmethod
    def update(product_data: dict) -> None:
        """Update product in database"""
        db.session.merge(product_data)
        db.session.commit()

    @staticmethod
    def delete(product_id: int) -> None:
        """Delete product from database"""
        item = db.session.query(ProductModel).filter_by(id=product_id).first()
        db.session.delete(item)
        db.session.commit()
