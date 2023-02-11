"""ORM Role model"""
from enum import Enum

from bookshop_app.database import db


class UserRole(Enum):
    """User roles"""

    ADMIN = "admin"
    MANAGER = "manager"
    CUSTOMER = "customer"


class RoleModel(db.Model):
    """Role ORM model"""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(UserRole), nullable=False)
