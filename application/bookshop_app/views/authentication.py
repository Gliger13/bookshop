"""Authentication views

Module contains routes for authentication blueprint, which includes the
functionality of user registration, login, log out functionality.
"""
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from bookshop_app.forms.authentication import LoginForm
from bookshop_app.forms.authentication import RegistrationForm
from bookshop_app.services.authentication import load_login_user

__all__ = ["authentication_blueprint"]

authentication_blueprint = Blueprint(
    name="authentication_blueprint", import_name=__name__, static_folder="static", template_folder="templates"
)


@authentication_blueprint.route("/login", methods=["GET"])
def login_page() -> str:
    """Route for the GET request to the login endpoint"""
    login_form = LoginForm()
    return render_template("authentication/login.html", user=current_user, form=login_form)


@authentication_blueprint.route("/login", methods=["POST"])
def login_post():
    """Route for the POST request to the login endpoint"""
    bearer = request.headers.get("Authorization")
    login_form = LoginForm()
    if not bearer:
        error = "Authorization header was not provided"
        render_template("authentication/login.html", user=current_user, form=login_form, error=error)

    token = bearer.split()[1]
    user = load_login_user(token)
    if not user:
        error = "Can not authenticate with provided authorization"
        return render_template("authentication/login.html", user=current_user, form=login_form, error=error)

    login_user(user, remember=True)
    return url_for("products_blueprint.products_page")


@authentication_blueprint.route("/log-out", methods=["POST"])
@login_required
def log_out_post():
    """Route for the POST request to the log-out endpoint"""
    logout_user()
    return redirect(url_for("authentication_blueprint.login_page"))


@authentication_blueprint.route("/registration", methods=["GET"])
def registration_page() -> str:
    """Route for the GET request to the registration endpoint"""
    registration_form = RegistrationForm()
    return render_template("authentication/registration.html", user=current_user, form=registration_form)


@authentication_blueprint.route("/registration", methods=["POST"])
def registration_post() -> Response | str:
    """Route for the POST request to the registration endpoint"""
    registration_form = RegistrationForm()
    if not registration_form.validate_on_submit():
        return render_template("authentication/registration.html", user=current_user, form=registration_form)
    return login_post()
