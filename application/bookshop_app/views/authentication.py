"""Authentication views

Module contains routes for authentication blueprint, which includes the
functionality of user registration, login, log out functionality.
"""
from requests import codes

from bookshop_app.controllers.user import UserController
from flask import Blueprint, redirect, render_template, request, Response, url_for

from bookshop_app.forms.authentication import LoginForm, RegistrationForm
from bookshop_app.services.authentication import verify_password

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
    login_form = LoginForm()
    return render_template("authentication/login.html", form=login_form)


@authentication_blueprint.route("/login", methods=["POST"])
def login_post():
    """Route for the POST request to the login endpoint"""
    login_form = LoginForm()
    if login_form.validate_on_submit() and \
            verify_password(login_form.data.get("login"), login_form.data.get("password")):
        return redirect(url_for("products_blueprint.products_page"))
    return render_template("authentication/login.html", form=login_form, error="Invalid user credentials")


@authentication_blueprint.route("/log-out", methods=["POST"])
def log_out_post() -> str:
    """Route for the POST request to the log-out endpoint"""
    raise NotImplementedError()


@authentication_blueprint.route("/registration", methods=["GET"])
def registration_page() -> str:
    """Route for the GET request to the registration endpoint"""
    registration_form = RegistrationForm()
    return render_template("authentication/registration.html", form=registration_form)


@authentication_blueprint.route("/registration", methods=["POST"])
def registration_post() -> Response | str:
    """Route for the POST request to the registration endpoint"""
    registration_form = RegistrationForm()
    if not registration_form.validate_on_submit():
        return render_template("authentication/registration.html", form=registration_form)

    create_user_response_data, status_code = UserController.create()
    if status_code is not codes.created:
        error = create_user_response_data.json.get("error", "Failed to create new user")
        return render_template("authentication/registration.html", form=registration_form, error=error)

    return redirect(url_for("products_blueprint.products_page"))
