"""Main application module"""
from importlib.resources import files

import connexion
from flask import Flask
from flask_migrate import Migrate

from bookshop_app.authenticator import verify_password
from bookshop_app.config import Config, get_environment_config_reference
from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.utils.logger import initialize_logger


def create_app() -> Flask:
    """Factory method for Flask provider"""

    options = {"swagger_ui": True}
    connexion_app = connexion.App(
        import_name="__name__",
        specification_dir=str(files("open_api")),
        options=options
    )
    connexion_app.add_api("swagger.yml")
    application = connexion_app.app
    application.config.from_object(get_environment_config_reference())
    db.init_app(application)
    ma.init_app(application)

    with application.app_context():
        db.create_all()
        return application


def basic_auth(username, password):
    if verify_password(username, password):
        return {"sub": username}
    return None


initialize_logger(Config.ENV)
app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
