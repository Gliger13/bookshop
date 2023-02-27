"""Authenticator service module"""
from typing import Optional

from flask_httpauth import HTTPBasicAuth
from werkzeug.datastructures import Authorization
from werkzeug.exceptions import Unauthorized

from bookshop_app.data_access_objects.user import UserDAO
from bookshop_app.dependencies import login_manager
from bookshop_app.models.user import UserModel

auth = HTTPBasicAuth()


def basic_auth(username: str, password: str) -> None | dict[str, str]:
    """Basic authentication

    Verify that the given username has a valid password provided, and return
    a basic authentication token if verification is successful, otherwise
    return None.

    :param username: user to authenticate
    :param password: password for the given username to verify
    :return: None if verification failed else authentication
    """
    if verify_password(username, password):
        return {"sub": username}
    return None


def jwt_authentication(token: str) -> Optional[dict]:
    """Try to decode provided JWT token and return its decoded data

    :param token: JWT token to decode
    :return: decoded token attributes or None
    """
    try:
        return UserModel.decode_token(token)
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
        model_id = jwt_token.get('sub')
        return UserModel.query.get(int(model_id))
    return None


@auth.verify_password
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


@auth.get_user_roles
def get_user_roles(user_authorization: Authorization) -> str:
    """Get all user role names to check role based authentication

    :param user_authorization: user authorization
    :return: user role
    """
    user = UserDAO.get_by_login(user_authorization.username)
    return user.role.name.name
