"""Module to manage ORM User model"""

import hashlib
import os

from bookshop_app.database import db


class User(db.Model):
    """User table specification"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(256), unique=True, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    password_hash = db.Column(db.String(64))

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
