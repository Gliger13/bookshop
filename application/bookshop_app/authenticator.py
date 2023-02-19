"""Authenticator module"""
import logging
from typing import Generator

from flask_httpauth import HTTPBasicAuth
from werkzeug.datastructures import Authorization

from bookshop_app.models.user import UserModel

auth = HTTPBasicAuth()


def basic_auth(username: str, password: str) -> None | dict[str, str]:
    """Basic authentication

    :param username: user to authenticate
    :param password: password for the given username to verify
    :return: None if verification failed else authentication
    """
    if verify_password(username, password):
        return {"sub": username}
    return None


@auth.verify_password
def verify_password(login: str, password: str) -> bool:
    """Verify given password for given login

    :param login: user login
    :param password: user login for password to verify
    :return: True if given password valid for given login else False
    """
    user = UserModel.query.filter_by(login=login).first()
    if not user or not user.verify_password(password):
        return False
    return True


@auth.get_user_roles
def get_user_roles(user_authorization: Authorization) -> str:
    """Get all user role names to check role based authentication

    :param user_authorization: user authorization
    :return: user role
    """
    user = UserModel.query.filter_by(login=user_authorization.username).first()
    return user.role.name.value
