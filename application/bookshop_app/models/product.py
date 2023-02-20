"""ORM Product Model"""

from bookshop_app.database.database import db


class ProductModel(db.Model):
    """Product model"""

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    author = db.Column(db.String(256))
    price = db.Column(db.Float)
    image_path = db.Column(db.String(256))
