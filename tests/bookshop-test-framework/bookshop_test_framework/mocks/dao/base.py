"""Base fake data access object"""
from abc import ABCMeta

from flask_sqlalchemy.model import Model


class BaseFakeDAO(metaclass=ABCMeta):
    """Base fake data access object"""

    __slots__ = ["_data"]

    _data: dict[Model]
