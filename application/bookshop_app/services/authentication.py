"""Authenticator service module"""
from functools import wraps
from typing import Any, Callable, Collection, Final, Optional
from flask_login import current_user
from flask import jsonify, request, Response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from requests import codes
from werkzeug.datastructures import Authorization
from werkzeug.exceptions import Unauthorized

from bookshop_app.data_access_objects.booking import BookingDAO
from bookshop_app.data_access_objects.user import UserDAO
from bookshop_app.dependencies import login_manager
from bookshop_app.models.role import UserRole
from bookshop_app.models.user import UserModel

ACCESS_DENIED_RESPONSE_JSON: Final[dict[str, str]] = {"status": codes.forbidden, "detail": "Access Denied"}

http_basic_auth = HTTPBasicAuth()
http_token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(http_basic_auth, http_token_auth)


def basic_authentication(username: str, password: str) -> None | dict[str, str]:
    """Basic authentication

    Verify that the given username has a valid password provided, and return
    a basic authentication token in RFC7662 format if verification is
    successful, otherwise return None.

    :param username: user to authenticate
    :param password: password for the given username to verify
    :return: None if verification failed else authentication
    """
    if verify_password(username, password):
        return {"sub": username}
    return None


def jwt_authentication(token: str) -> Optional[dict]:
    """JWT authentication

    Try to decode provided JWT token and return its decoded data in RFC7662
    format if verification is successful, otherwise return None.

    :param token: JWT token to decode
    :return: decoded token attributes or None
    """
    try:
        return UserModel.decode_token(token)
    except Unauthorized:
        return None


@http_token_auth.verify_token
def verify_jwt_token(token: str) -> Optional[str]:
    """Try to decode provided JWT token and return its decoded data

    :param token: JWT token to decode
    :return: username from the decoded token
    """
    try:
        return UserModel.decode_token(token).get("sub")
    except Unauthorized:
        return None


@login_manager.user_loader
def load_login_user(token: str) -> Optional[UserModel]:
    """Loads user based on the given JWT token

    Try to get decoded data from the provided JWT token. If successful, get and
    return user model that provided token belongs to, otherwise return None.

    :param token: JWT token for user to get
    :return: user model that provided token belongs to
    """
    if jwt_token := jwt_authentication(token):
        if user_login := jwt_token.get('sub'):
            return UserDAO.get_by_login(user_login)
    return None


@http_basic_auth.verify_password
def verify_password(login: str, password: str) -> bool:
    """Verify given password for given login

    :param login: user login
    :param password: user login for password to verify
    :return: True if given password valid for given login else False
    """
    user = UserDAO.get_by_login(login)
    if not user or not user.verify_password(password):
        return False
    return True


@http_basic_auth.get_user_roles
def __get_user_roles_for_basic_auth(user_authorization: Authorization) -> UserRole:
    """Get all user role names to check role based authentication

    :param user_authorization: user authorization
    :return: user role
    """
    user = UserDAO.get_by_login(user_authorization.username)
    return user.role.name


@http_token_auth.get_user_roles
def __get_user_roles_for_token_auth(username: str) -> UserRole:
    """Get all user role names to check role based authentication

    :param username: user authorization
    :return: user role
    """
    user = UserDAO.get_by_login(username)
    return user.role.name


def required_roles(roles: Collection[object]) -> Callable:
    """User required to have listed roles

    :param roles: collection of roles to have to access function
    :return: result of wrapped function if access granted
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> tuple[Response | dict, int]:
            user = __get_current_user()
            if user.role.name in roles:
                return function(*args, **kwargs)
            return jsonify(**ACCESS_DENIED_RESPONSE_JSON), codes.forbidden

        return wrapper

    return decorator


def required_same_user_id_or_roles(roles: Collection[object] = ()) -> Callable:
    """User required to use only same user id or have listed roles

    :param roles: collection of roles to have to access function
    :return: result of wrapped function if access granted
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(user_id: int, *args: Any, **kwargs: Any) -> tuple[Response | dict, int]:
            user = __get_current_user()
            if user.id == user_id:
                return function(user_id, *args, **kwargs)
            if user.role.name in roles:
                return function(user_id, *args, **kwargs)
            return jsonify(**ACCESS_DENIED_RESPONSE_JSON), codes.forbidden

        return wrapper

    return decorator


def filter_bookings_by_roles(roles: Collection[object] = ()) -> Callable:
    """Filter requested bookings by access role

    :param roles: collection of roles to have to access function
    :return: result of wrapped function if access granted
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> tuple[Response | dict, int]:
            bookings_data, status_code = function(*args, **kwargs)
            user = __get_current_user()
            if user.role.name in roles:
                return bookings_data, status_code
            return jsonify([booking for booking in bookings_data if booking.get("user_id") == user.id]), status_code

        return wrapper

    return decorator


def required_own_given_booking_id_or_roles(roles: Collection[object] = ()) -> Callable:
    """User required to use only own booking id or have listed roles

    :param roles: collection of roles to have to access function
    :return: result of wrapped function if access granted
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(booking_id: int, *args: Any, **kwargs: Any) -> tuple[Response | dict, int]:
            user = __get_current_user()
            booking = BookingDAO.get_by_id(booking_id)
            if booking and user.id == booking.user_id:
                return function(booking_id, *args, **kwargs)
            if user.role.name in roles:
                return function(booking_id, *args, **kwargs)
            return jsonify(**ACCESS_DENIED_RESPONSE_JSON), codes.forbidden

        return wrapper

    return decorator


def required_creating_booking_for_self_or_roles(roles: Collection[object] = ()) -> Callable:
    """User required to create booking only for self or have listed roles

    :param roles: collection of roles to have to access function
    :return: result of wrapped function if access granted
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> tuple[Response | dict, int]:
            if not request.is_json:
                return function(*args, **kwargs)

            user_id_to_create_booking = request.json.get("user_id")
            if not user_id_to_create_booking:
                return function(*args, **kwargs)

            user = __get_current_user()
            if user.id == user_id_to_create_booking:
                return function(*args, **kwargs)

            if user.role.name in roles:
                return function(*args, **kwargs)
            return jsonify(**ACCESS_DENIED_RESPONSE_JSON), codes.forbidden

        return wrapper

    return decorator


def __get_current_user() -> Optional[UserModel]:
    """Get current user for authentication and access control

    :return: current user model
    """
    if username := multi_auth.current_user():
        return UserDAO.get_by_login(username)
    return current_user
