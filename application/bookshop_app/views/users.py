"""Users views

Module contains routes for the users blueprint, which includes the
functionality of creating, reading, updating, and deleting all users.
"""

from flask import Blueprint, render_template

from flask_login import current_user

__all__ = ["users_blueprint"]

users_blueprint = Blueprint(
    name="users_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@users_blueprint.route("/users", methods=["GET"])
def users_page() -> str:
    """Route for the GET request to the users endpoint"""
    return render_template("users/users.html", user=current_user)


@users_blueprint.route("/user/<user_id>", methods=["GET"])
def user_page(user_id: str) -> str:
    """Route for the GET request to the user endpoint"""
    return render_template("users/user.html", user=current_user)


@users_blueprint.route("/user/<user_id>", methods=["POST"])
def user_post(user_id: str) -> str:
    """Route for the POST request to the user endpoint"""
    raise NotImplementedError()


@users_blueprint.route("/user/<user_id>", methods=["PUT"])
def user_update(user_id: str) -> str:
    """Route for the PUT request to the user endpoint"""
    raise NotImplementedError()


@users_blueprint.route("/user/<user_id>", methods=["DELETE"])
def user_delete(user_id: str) -> str:
    """Route for the DELETE request to the user endpoint"""
    raise NotImplementedError()
