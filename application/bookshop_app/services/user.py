"""User service

Module contains User Service that provides methods with CRUD operations for
user resource.
"""

from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.user import UserDAO
from bookshop_app.schemas.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserService:
    """User Service

    Provides service methods that support CRUD operations for user resource
    """

    @staticmethod
    def get(user_id: int) -> dict:
        """Get user resource"""
        user_data = UserDAO.get_by_id(user_id)
        return user_schema.dump(user_data)

    @staticmethod
    def get_all() -> list[dict]:
        """Get all user resources"""
        all_users_data = UserDAO.get_all()
        return user_list_schema.dump(all_users_data)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create user resource"""
        user_req_json = request.get_json()
        password = user_req_json.pop('password', None)
        if not password:
            return jsonify(
                detail='Impossible to create a new user. Field "password" is not set.',
                status=codes.bad_request,
                title="Bad Request",
                type="about:blank",
            )
        user_data = user_schema.load(user_req_json)
        user_data.hash_password(password)
        UserDAO.create(user_data)
        return user_schema.dump(user_data), codes.created

    @staticmethod
    def delete(user_id: int) -> tuple[dict[str, str], int]:
        """Delete user resource"""
        UserDAO.get_by_id(user_id)
        UserDAO.delete(user_id)
        return {'message': 'User deleted successfully'}, codes.ok

    @staticmethod
    def update(user_id: int) -> Response | tuple[dict, int]:
        """Update user resource"""
        try:
            user_data = user_schema.dump(UserDAO.get_by_id(user_id))
            user_data.update(request.get_json())
            user_data = user_schema.load(user_data)
            UserDAO.update(user_data)
            return user_schema.dump(user_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request, title="Bad Request", type="about:blank")
