"""Module with dependencies instantiations"""
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

ma = Marshmallow()
login_manager = LoginManager()
login_manager.login_view = 'authentication_blueprint.login_page'
