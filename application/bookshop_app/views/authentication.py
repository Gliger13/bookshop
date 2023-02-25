"""Authentication views

Module contains routes for authentication blueprint, which includes the
functionality of user registration, login, log out functionality.
"""
from flask import Blueprint, render_template

__all__ = ["authentication_blueprint"]

authentication_blueprint = Blueprint(
    name="authentication_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@authentication_blueprint.route("/login", methods=["GET"])
def login_page() -> str:
    """Route for the GET request to the login endpoint"""
    return render_template("authentication/login.html")


@authentication_blueprint.route("/login", methods=["POST"])
def login_post() -> str:
    """Route for the POST request to the login endpoint"""
    raise NotImplementedError()


@authentication_blueprint.route("/log-out", methods=["POST"])
def log_out_post() -> str:
    """Route for the POST request to the log-out endpoint"""
    raise NotImplementedError()


@authentication_blueprint.route("/registration", methods=["GET"])
def registration_page() -> str:
    """Route for the GET request to the registration endpoint"""
    return render_template("authentication/registration.html")


@authentication_blueprint.route("/registration", methods=["POST"])
def registration_post() -> str:
    """Route for the POST request to the registration endpoint"""
    raise NotImplementedError()
