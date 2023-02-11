"""ORM User Model"""

import hashlib
import os

from bookshop_app.database import db
from bookshop_app.models.role import RoleModel


class UserModel(db.Model):
    """User ORM model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship(RoleModel.__name__)

    name = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(256), unique=True)
    address = db.Column(db.String(256))

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def hash_password(self, password: str):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password_hash = salt + key

    def verify_password(self, password: str):
        salt, key = self.password_hash[:32], self.password_hash[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return key == new_key
