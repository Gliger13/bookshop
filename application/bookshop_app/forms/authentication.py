"""Authentication forms

Module contains WTF-forms for user authentication, which includes user login,
registration and update.
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    """Login form with login and password fields"""

    login = StringField("login", validators=[validators.input_required(), validators.length(min=4, max=256)])
    password = PasswordField("password", validators=[validators.input_required(), validators.length(min=8, max=256)])
