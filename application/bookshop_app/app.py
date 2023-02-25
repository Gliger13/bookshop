#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main application module"""
from importlib.resources import files

import connexion
from flask import Flask
from flask_migrate import Migrate

from bookshop_app.config import Config, get_environment_config_reference
from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.routes.booking import booking_control, booking_manipulation
from bookshop_app.routes.product import product_control, product_manipulation
from bookshop_app.routes.store_item import store_item_control, store_item_manipulation
from bookshop_app.routes.user import user_control, user_manipulation
from bookshop_app.utils.logger import initialize_logger
from bookshop_app.views.blueprints import register_all_blueprints


def create_app() -> Flask:
    """Factory method for Flask provider"""

    options = {"swagger_ui": True}
    connexion_app = connexion.App(
        import_name="__name__",
        specification_dir=str(files("bookshop_app").joinpath("open_api")),
        options=options
    )
    connexion_app.add_api("swagger.yml")
    application = connexion_app.app
    application.config.from_object(get_environment_config_reference())
    register_all_blueprints(application)
    db.init_app(application)
    ma.init_app(application)

    with application.app_context():
        db.create_all()
        return application


def add_routes(application: Flask) -> None:
    """Add routes for all models to the current application

    :param application: flask application to add routes
    """
    application.add_url_rule(
        rule="/user", methods=["GET", "POST"], view_func=user_control)
    application.add_url_rule(
        rule="/user/<int:user_id>", methods=["GET", "PUT", "DELETE"], view_func=user_manipulation)
    application.add_url_rule(
        rule="/product", methods=["GET", "POST"], view_func=product_control)
    application.add_url_rule(
        rule="/product/<int:product_id>", methods=["GET", "PUT", "DELETE"], view_func=product_manipulation)
    application.add_url_rule(
        rule="/booking", methods=["GET", "POST"], view_func=booking_control)
    application.add_url_rule(
        rule="/booking/<int:booking_id>", methods=["GET", "PUT", "DELETE"], view_func=booking_manipulation)
    application.add_url_rule(
        rule="/user", methods=["GET", "POST"], view_func=store_item_control)
    application.add_url_rule(
        rule="/user/<int:user_id>", methods=["GET", "PUT", "DELETE"], view_func=store_item_manipulation)


initialize_logger(Config.ENV)
app = create_app()
migrate = Migrate(app, db)


def run_application() -> None:
    """Run application"""
    app.run()


if __name__ == "__main__":
    run_application()
