"""Logger configuration and initialization"""
import logging

from bookshop_app.config import Environment


def initialize_logger(environment_name: str) -> None:
    """Initialize package logger depends on environment type

    :param environment_name: current environment name
    """
    logger = logging.getLogger()
    if environment_name == Environment.DEVELOPMENT.name:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
