"""Main application module"""

import connexion
from flask import Flask
from flask_migrate import Migrate

from bookshop_app.authenticator import verify_password
from bookshop_app.config import get_environment_config
from bookshop_app.database import db
from bookshop_app.dependencies import ma


def create_app() -> Flask:
    """Factory method for Flask provider"""

    options = {'swagger_ui': True}
    connexion_app = connexion.App("__name__",
                                  specification_dir='./open_api/',
                                  options=options)
    connexion_app.add_api('swagger.yml')
    application = connexion_app.app
    application.config.from_object(get_environment_config())
    db.init_app(application)
    ma.init_app(application)

    with application.app_context():
        db.create_all()
        return application


def basic_auth(username, password):
    if verify_password(username, password):
        return {"sub": username}
    return None


app = create_app()
migrate = Migrate(app, db, render_as_batch=True)

if __name__ == "__main__":
    app.run()
