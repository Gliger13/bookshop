"""Authenticator module"""
from flask_httpauth import HTTPBasicAuth

from bookshop_app.models.user import UserModel

auth = HTTPBasicAuth()


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
