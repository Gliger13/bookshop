"""Module to store environment configs"""

import os

import click


class Config(object):
    """Parent class for environment configs"""

    ENV = os.environ["ENV"] if "ENV" in os.environ else "DEVELOPMENT"
    CSRF_ENABLED = True
    SECRET_KEY = "this_is_a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development environment config"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    click.echo(SQLALCHEMY_DATABASE_URI)


class TestingConfig(Config):
    """Test environment config"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


def get_environment_config() -> str:
    """To supports several environments"""

    if Config.ENV == "TESTING":
        return "config.TestingConfig"
    elif Config.ENV == "DEVELOPMENT":
        return "config.DevelopmentConfig"
