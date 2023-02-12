"""User routes

Module contains routes for user manipulations.
"""

from flask import request, Response

from bookshop_app.controllers.user import UserController


def user_control() -> tuple[Response | dict | list[dict], int]:
    """URL to collect information about users or create new one

    :return: tuple of response json and status code
    """
    if request.method == "POST":
        return UserController.create()
    else:
        return UserController.get_all()


def user_manipulation(user_id: int) -> tuple[Response | dict | list[dict], int]:
    """URL to get, update or delete user information

    :param user_id: ID of the user to manipulate
    :return: tuple of response json and status code
    """
    if request.method == "GET":
        return UserController.get(user_id)
    elif request.method == "PUT":
        return UserController.update(user_id)
    else:
        return UserController.delete(user_id)
