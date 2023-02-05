"""
Module for User Data Access Object
"""

from typing import List

from bookshop_app.database import db
from bookshop_app.models.user_model import User


class UserDao:
    """
    Data Access Object class for User Model
    """

    USER_NOT_FOUND = "User not found for id: {}"

    @staticmethod
    def create(user: User):
        """Creates user in database"""
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def fetch_by_id(user_id: int) -> User:
        """Gets user by id from database"""
        return db.session.query(User).get_or_404(
            user_id,
            description=UserDao.USER_NOT_FOUND.format(user_id)
        )

    @staticmethod
    def fetch_all() -> List[User]:
        """Returns all users from database"""
        return db.session.query(User).all()

    @staticmethod
    def delete(user_id) -> None:
        """Deletes user from database"""
        item = db.session.query(User).filter_by(id=user_id).first()
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def update(user_data):
        """Updates user in database"""
        db.session.merge(user_data)
        db.session.commit()
