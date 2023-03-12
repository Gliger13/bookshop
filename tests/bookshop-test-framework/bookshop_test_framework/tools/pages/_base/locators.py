"""Abstract base page locators"""
from abc import ABCMeta
from collections import namedtuple

Locator = namedtuple("Locator", ["by", "value"])


class BasePageLocators(metaclass=ABCMeta):
    """Responsible for storing UI page locators"""

    __slots__ = []
