"""Module to store environment configs"""
import importlib
import logging
import os
from abc import ABCMeta
from enum import Enum
from functools import lru_cache
from importlib.resources import files

import click


class ConfigError(Exception):
    """Custom error for all config related errors"""

    def __init__(self, message: str):
        """Initialize configuration error with the given message"""
        self.message = message


class Environment(Enum):
    """Describes all environment types"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Config(metaclass=ABCMeta):
    """Parent class for environment configs"""

    ENV = os.environ["ENV"] if "ENV" in os.environ else "DEVELOPMENT"
    CSRF_ENABLED = True
    SECRET_KEY = "this_is_a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development environment config"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    FILE_MANAGER_CONFIG = {
        "manager_type": "local",
        "dir_to_save": files("instance").joinpath("files")
    }
    click.echo(SQLALCHEMY_DATABASE_URI)


class TestingConfig(Config):
    """Test environment config"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    FILE_MANAGER_CONFIG = {
        "manager_type": "local",
        "dir_to_save": files("instance").joinpath("files")
    }


class ProductionConfig(Config):
    """Test environment config"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    FILE_MANAGER_CONFIG = {
        "manager_type": "local",
        "dir_to_save": files("instance").joinpath("files")
    }


def get_environment_config_reference() -> str:
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


@lru_cache
def get_environment_config() -> Config:
    """Get environment config object for the current environment

    :return: config for the current environment
    """
    current_environment_config_reference = get_environment_config_reference()
    split_config_path = current_environment_config_reference.split(".")
    module_path = ".".join(split_config_path[:-1])
    config_class_name = split_config_path[-1]
    module_with_config = importlib.import_module(module_path)
    return getattr(module_with_config, config_class_name)
