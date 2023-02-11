"""Module to store environment configs"""
import logging
import os
from enum import Enum

import click


class Environment(Enum):
    """Describes all environment types"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


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


class ProductionConfig(Config):
    """Test environment config"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


def get_environment_config() -> str:
    """Get environment config depends on environment name

    :return: package path for config for the current environment type
    """
    logging.info("Loading application config for `%s` environment", Config.ENV)
    match Config.ENV:
        case Environment.DEVELOPMENT.name:
            return "config.DevelopmentConfig"
        case Environment.TESTING.name:
            return "config.TestingConfig"
        case Environment.PRODUCTION.name:
            return "config.ProductionConfig"
        case _:
            raise EnvironmentError(
                f"Invalid environment name `{Config.ENV}` specified in environment variables. "
                f"Please specify any of {[env.name for env in Environment]}")
