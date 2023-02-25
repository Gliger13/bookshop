from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    login = StringField("login", validators=[validators.input_required(), validators.length(max=256)])
    password = PasswordField("password")
