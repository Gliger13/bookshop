"""User Data Access Object"""

from bookshop_app.database.database import db
from bookshop_app.models.user import UserModel


class UserMessages:
    """User messages and templates"""

    USER_NOT_FOUND = "User not found for id: {user_id}"


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
            description=UserMessages.USER_NOT_FOUND.format(user_id=user_id))

    @staticmethod
    def get_all() -> list[UserModel]:
        """Return all users from database"""
        return db.session.query(UserModel).all()

    @staticmethod
    def delete(user_id) -> None:
        """Delete user from database"""
        item = db.session.query(UserModel).filter_by(id=user_id).first()
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def update(user_data) -> None:
        """Update user in database"""
        db.session.merge(user_data)
        db.session.commit()
