"""Services module"""
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.user_dao import UserDao
from bookshop_app.models.user_schema import UserSchema

userSchema = UserSchema()
userListSchema = UserSchema(many=True)


class UserService:
    """To support CRUD operations for user resource"""

    @staticmethod
    def get(user_id: int):
        """Get user resource"""
        user_data = UserDao.fetch_by_id(user_id)
        return userSchema.dump(user_data)

    @staticmethod
    def get_all():
        """Get all user resources"""
        return userListSchema.dump(UserDao.fetch_all())

    @staticmethod
    def create():
        """Create user resource"""
        user_req_json = request.get_json()
        password = user_req_json.pop('password', None)
        if not password:
            return jsonify(detail='Impossible to create a new user. Field "password" is not set.',
                           status=400, title="Bad Request", type="about:blank")
        user_data = userSchema.load(user_req_json)
        user_data.hash_password(password)
        UserDao.create(user_data)
        return userSchema.dump(user_data), 201

    @staticmethod
    def delete(user_id: int):
        """Delete user resource"""
        UserDao.fetch_by_id(user_id)
        UserDao.delete(user_id)
        return {'message': 'User deleted successfully'}, 200

    @staticmethod
    def update(user_id: int):
        """Update user resource"""
        try:
            user_data = userSchema.dump(UserDao.fetch_by_id(user_id))
            user_data.update(request.get_json())
            user_data = userSchema.load(user_data)
            UserDao.update(user_data)
            return userSchema.dump(user_data), 200
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")
