"""User Data Access Object"""
from typing import Final, Optional

from bookshop_app.database.database import db
from bookshop_app.models.user import UserModel

USER_NOT_FOUND: Final = "User not found for id: {user_id}"


class UserDAO:
    """Data Access Object class for User Model"""

    @staticmethod
    def create(user: UserModel) -> None:
        """Create user in database"""
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id: int) -> UserModel:
        """Get user by id from database"""
        return db.session.query(UserModel).get_or_404(
            user_id,
            description=USER_NOT_FOUND.format(user_id=user_id))

    @staticmethod
    def get_by_login(user_login: str) -> Optional[UserModel]:
        """Get user by login from database"""
        return db.session.query(UserModel).filter_by(login=user_login).first()

    @staticmethod
    def get_all() -> list[UserModel]:
        """Return all users from database"""
        return db.session.query(UserModel).all()

    @staticmethod
    def delete(user_id: int) -> None:
        """Delete user from database"""
        item = db.session.query(UserModel).filter_by(id=user_id).first()
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def update(updated_user: UserModel) -> None:
        """Update user in database"""
        db.session.merge(updated_user)
        db.session.commit()
