"""ORM User Model"""

import hashlib
import os

from bookshop_app.database.database import db
from bookshop_app.models.role import RoleModel


class UserModel(db.Model):
    """User ORM model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey(f"{RoleModel.__tablename__}.id"), nullable=False)
    role = db.relationship(RoleModel.__name__)

    name = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(256), unique=True)
    address = db.Column(db.String(256))

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def hash_password(self, password: str) -> None:
        """Hash given password and set hashed password to the user model

        :param password: password to hash and set
        """
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password_hash = salt + key

    def verify_password(self, password: str) -> bool:
        """Verify given password matches current user hashed password

        :param password: password to hash and verify
        :return: True if the given hashed password matches hashed current
        """
        salt, key = self.password_hash[:32], self.password_hash[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return key == new_key