"""Bookshop application fixtures"""
import pytest
from flask import Flask
from flask.testing import FlaskClient

from bookshop_app.app import create_app


@pytest.fixture(scope="session")
def application() -> Flask:
    """Initialize and return bookshop testing application"""
    app = create_app()
    app.config.from_object("bookshop_app.config.TestingConfig")
    app.config.update({
        "TESTING": True,
    })
    return app


@pytest.fixture(scope="session")
def application_client(application: Flask) -> FlaskClient:
    """Get application testing client"""
    return application.test_client()
