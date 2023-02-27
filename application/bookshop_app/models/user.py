"""ORM User Model"""

import hashlib
import os
import time
from typing import Final, Optional

import jwt
from flask_login import UserMixin
from werkzeug.exceptions import Unauthorized

from bookshop_app.database.database import db
from bookshop_app.models.role import RoleModel


class UserModel(UserMixin, db.Model):
    """User ORM model"""

    JWT_LIFETIME_SECONDS: Final[int] = 600
    JWT_ALGORITHM: Final[str] = "HS256"

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey(f"{RoleModel.__tablename__}.id"), default=3)
    role = db.relationship(RoleModel.__name__)

    name = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(256), unique=True)
    address = db.Column(db.String(256))

    token: Optional[str] = None

    def get_id(self) -> str:
        """Get user ID for Login Manager"""
        if self.token:
            try:
                self.decode_token(self.token)
            except Unauthorized:
                self.generate_token()
        else:
            self.generate_jwt_token()
        return self.token

    def __repr__(self) -> str:
        return f"<User {self.login}>"

    def hash_password(self, password: str) -> None:
        """Hash given password and set hashed password to the user model

        :param password: password to hash and set
        """
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        self.password_hash = salt + key

    def verify_password(self, password: str) -> bool:
        """Verify given password matches current user hashed password

        :param password: password to hash and verify
        :return: True if the given hashed password matches hashed current
        """
        salt, key = self.password_hash[:32], self.password_hash[32:]
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return key == new_key

    def generate_jwt_token(self) -> str:
        """Generates JWT token"""
        timestamp = int(time.time())
        payload = {
            "iat": int(timestamp),
            "exp": int(timestamp + self.JWT_LIFETIME_SECONDS),
            "sub": str(self.id),
        }
        self.token = jwt.encode(payload, "SECRET_KEY", algorithm=self.JWT_ALGORITHM)
        return self.token

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """Decode and return data from the given JWT token

        :raise Unauthorized: if the token is invalid
        :param token: token to decode
        :return: decoded data from the given JWT token
        """
        try:
            return jwt.decode(token, "SECRET_KEY", algorithms=[cls.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Signature expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid token. Please log in again.")
        except TypeError:
            raise Unauthorized("Invalid token. Please log in again.")
