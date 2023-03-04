"""Authentication forms

Module contains WTF-forms for user authentication, which includes user login,
registration and update.
"""
from collections import namedtuple

from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, PasswordField, StringField, validators

from bookshop_app.models.role import UserRole

FieldProtocol = namedtuple("FieldProtocol", ["label", "validators"])


class UserForm:
    """Abstract form describes all user properties"""

    id = FieldProtocol(label="ID", validators=[])
    login = FieldProtocol(label="Login", validators=[validators.length(min=4, max=256)])
    password = FieldProtocol(label="Password", validators=[validators.length(min=8, max=256)])
    email = FieldProtocol(label="Email", validators=[])
    phone = FieldProtocol(
        label="Phone", validators=[validators.regexp(r"(^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$)*")])
    name = FieldProtocol(label="First and Last name", validators=[validators.length(max=256)])
    address = FieldProtocol(label="Address", validators=[validators.length(max=256)])
    role_id = FieldProtocol(label="Role ID", validators=[validators.number_range(1, len(UserRole))])


class LoginForm(FlaskForm):
    """Login form with login and password fields"""
    __base = UserForm()

    login = StringField(__base.login.label, [validators.input_required(), *__base.login.validators])
    password = PasswordField(__base.password.label, [validators.input_required(), *__base.password.validators])


class RegistrationForm(FlaskForm):
    """Registration form for user"""
    __base = UserForm()

    login = StringField(__base.login.label, [validators.input_required(), *__base.login.validators])
    password = PasswordField(__base.password.label, [validators.input_required(), *__base.password.validators])
    email = EmailField(__base.email.label, [validators.input_required(), *__base.email.validators])
    phone = StringField(__base.phone.label, [validators.optional(), *__base.phone.validators])
    name = StringField(__base.name.label, [validators.optional(), *__base.name.validators])
    address = StringField(__base.address.label, [validators.optional(), *__base.address.validators])
    role_id = IntegerField(__base.role_id.label, [validators.optional(), *__base.role_id.validators])


class UpdateUserForm(FlaskForm):
    """Update user form"""
    __base = UserForm()

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.id.validators])
    login = StringField(__base.login.label, [validators.optional(), *__base.login.validators])
    password = PasswordField(__base.password.label, [validators.optional(), *__base.password.validators])
    email = EmailField(__base.email.label, [validators.optional(), *__base.email.validators])
    phone = StringField(__base.phone.label, [validators.optional(), *__base.phone.validators])
    name = StringField(__base.name.label, [validators.optional(), *__base.name.validators])
    address = StringField(__base.address.label, [validators.optional(), *__base.address.validators])
    role_id = IntegerField(__base.role_id.label, [validators.optional(), *__base.role_id.validators])


class DeleteUserForm(FlaskForm):
    """Update user form"""
    __base = UserForm()

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.id.validators])
