"""User service

Module contains User Service that provides methods with CRUD operations for
user resource.
"""
from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.role import RoleDAO
from bookshop_app.data_access_objects.user import UserDAO
from bookshop_app.schemas.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserService:
    """User Service

    Provides service methods that support CRUD operations for user resource
    """

    @staticmethod
    def get(user_id: int) -> tuple[dict, int]:
        """Get user resource with the given ID

        :param user_id: ID of the user resource to get
        :raise HTTPException: if user with the given ID does not exist
        :return: tuple of response json with user attributes and status code
        """
        user_data = UserDAO.get_by_id(user_id)
        return user_schema.dump(user_data), codes.ok

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all user resources

        :return: tuple of response json with all users and status code
        """
        all_users_data = UserDAO.get_all()
        return user_list_schema.dump(all_users_data), codes.ok

    @staticmethod
    def create() -> tuple[dict | Response, int]:
        """Create user resource

        Validate and load create user request json using User Schema. Validate
        request using custom schema validators. Check for role ID existence.
        Hash user password. Create User Model using Data Access Object.

        :raise HTTPException: raise if
          - there are validation errors with request json
          - role with the given ID does not exist
        :return: tuple of response json and status code
        """
        try:
            create_user_request_json = request.get_json()
            password_to_hash = create_user_request_json.pop("password")

            user_data = user_schema.load(create_user_request_json)
            UserService.validate_user_creation_request({**create_user_request_json, "password": password_to_hash})

            user_data.hash_password(password_to_hash)
            UserDAO.create(user_data)
            return user_schema.dump(user_data), codes.created
        except ValidationError as error:
            return jsonify(error=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(error=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def validate_user_creation_request(create_user_request_json: dict) -> None:
        """Validate user creation request json

        Checks given user relationship model instances exists. Triggers custom
        schema validations.

        :param create_user_request_json: dict with request json to create user
        :raise ValidationError: if there are validations errors with given json
        :raise HTTPException: if role ID was provided, but it does not exist
        """
        user_schema.validate_password(create_user_request_json.get("password"))
        RoleDAO.get_by_id(create_user_request_json.get("role_id"))

    @staticmethod
    def delete(user_id: int) -> tuple[dict[str, str], int]:
        """Delete user resource

        Check if user with the given ID exists. Delete User Model with given ID
        using Data Access Object.

        :raise HTTPException: if the user does not exist with the given ID
        :return: tuple of response json and status code
        """
        UserDAO.get_by_id(user_id)
        UserDAO.delete(user_id)
        return {"message": "User deleted successfully"}, codes.ok

    @staticmethod
    def update(user_id: int) -> tuple[dict | Response, int]:
        """Update user resource with the given ID

        Check if user with the given ID exists. Merge old user data with new
        data from the update user request json. Validate and load merged data
        using user schema. Validate data using custom schema validators. Check
        if role with the given ID role id exists if it was provided. Hash
        user's password if it was provided. Update User Model using Data Access
        Object.

        :raise HTTPException: raise if
          - there are validation errors with request json
          - user with the given ID does not exist
          - role with the given ID does not exist
        :return: tuple of response json and status code
        """
        try:
            user_model_to_update = UserDAO.get_by_id(user_id)
            update_user_request_json = request.get_json()

            UserService.validate_user_update_request(update_user_request_json)

            if password_to_update := update_user_request_json.pop("password", None):
                user_model_to_update.hash_password(password_to_update)
            user_data_to_update = user_schema.dump(user_model_to_update)
            user_data_to_update.update(update_user_request_json)
            updated_user_data = user_schema.load(user_data_to_update)
            UserDAO.update(updated_user_data)
            return user_schema.dump(updated_user_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def validate_user_update_request(update_user_request_json: dict) -> None:
        """Validate user creation request json

        Checks given user relationship model instances exists. Triggers custom
        schema validations.

        :param update_user_request_json: dict with request json to update user
        :raise ValidationError: if there are validations errors with given json
        :raise HTTPException: if role with the given ID does not exist
        """
        if password_to_validate := update_user_request_json.get("password"):
            user_schema.validate_password(password_to_validate)
        if role_id_to_validate := update_user_request_json.get("role_id"):
            RoleDAO.get_by_id(role_id_to_validate)

    @staticmethod
    def generate_jwt_token() -> tuple[dict | Response, int]:
        """Generates JWT for the user and returns it."""
        login = request.authorization.username
        user = UserDAO.get_by_login(login)
        access_token = user.generate_jwt_token()
        return jsonify(AuthToken=access_token), codes.ok
