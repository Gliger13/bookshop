"""Blueprint related functions

Module contains functions for managing and interaction with all project related
blueprints.
"""
from flask import Flask

from bookshop_app.views.authentication import authentication_blueprint
from bookshop_app.views.bookings import bookings_blueprint
from bookshop_app.views.main import main_blueprint
from bookshop_app.views.media import media_blueprint
from bookshop_app.views.products import products_blueprint
from bookshop_app.views.store_items import store_items_blueprint
from bookshop_app.views.users import users_blueprint

__all__ = ["register_all_blueprints"]


def register_all_blueprints(application: Flask) -> None:
    """Register all project blueprints for the given application

    :param application: application for registering blueprints
    """
    application.register_blueprint(main_blueprint)
    application.register_blueprint(users_blueprint)
    application.register_blueprint(authentication_blueprint)
    application.register_blueprint(products_blueprint)
    application.register_blueprint(bookings_blueprint)
    application.register_blueprint(store_items_blueprint)
    application.register_blueprint(media_blueprint)
