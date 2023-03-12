"""Base page object abstract class"""
from abc import ABCMeta

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage(metaclass=ABCMeta):
    """Abstract base page object pattern implementation"""

    __slots__ = ["_driver"]

    def __init__(self, driver: WebDriver) -> None:
        """Initialize page object with the given driver

        :param driver: selenium driver to use for ui interactions
        """
        self._driver = driver
