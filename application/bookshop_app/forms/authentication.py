"""Authentication forms

Module contains WTF-forms for user authentication, which includes user login,
registration and update.
"""
from flask_wtf import FlaskForm
from wtforms import EmailField, Field, PasswordField, StringField, ValidationError, validators


class LoginForm(FlaskForm):
    """Login form with login and password fields"""

    login = StringField("login", validators=[validators.input_required(), validators.length(min=4, max=256)])
    password = PasswordField("password", validators=[validators.input_required(), validators.length(min=8, max=256)])


class RegistrationForm(FlaskForm):
    """Registration form for user"""

    login = StringField(
        label="Login", validators=[validators.input_required(), validators.length(min=4, max=256)])
    password = PasswordField(
        label="Password", validators=[validators.input_required(), validators.length(min=8, max=256)])
    repeat_password = PasswordField(
        label="Repeat password", validators=[validators.input_required(), validators.length(min=8, max=256)])

    email = EmailField(
        label="Email", validators=[validators.input_required()])
    phone = StringField(
        label="Phone", validators=[validators.regexp(r"(^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$)*")])
    name = StringField(
        label="First and last name", validators=[validators.length(max=256)])
    address = StringField(
        label="Address", validators=[validators.length(max=256)])

    def validate_password(self, field: Field) -> None:
        if field.data != self.repeat_password.data:
            raise ValidationError("Entered passwords are not the same")
