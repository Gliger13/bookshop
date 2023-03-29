"""Base page elements classes

Module contains base page elements and their divergences.
"""
from abc import ABCMeta
from abc import abstractmethod
from functools import cached_property

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from bookshop_test_framework.tools.pages._base.locators import Locator
from bookshop_test_framework.tools.pages._base.wrappers import retry_on_selenium_error


class BasePageElement(metaclass=ABCMeta):
    """Abstract UI page element class for all elements"""

    __slots__ = ["_driver"]

    def __init__(self, driver: WebDriver) -> None:
        """Initialize page element with the given driver

        :param driver: selenium driver for interactions
        """
        self._driver = driver

    @abstractmethod
    @cached_property
    def locator(self) -> Locator:
        """Abstract property to return locator for the current page element"""

    @retry_on_selenium_error()
    def set(self, value: str) -> None:
        """Set given value for the current element on the page

        :param value: value to set for the element
        """
        WebDriverWait(self._driver, 100).until(lambda driver: driver.find_element(*self.locator))
        self._driver.find_element(*self.locator).clear()
        self._driver.find_element(*self.locator).send_keys(value)

    @retry_on_selenium_error()
    def get(self) -> str:
        """Get element value from the current ui element

        :return: current page element value
        """
        WebDriverWait(self._driver, 100).until(lambda driver: driver.find_element(*self.locator))
        element = self._driver.find_element(*self.locator)
        return element.get_attribute("value")


class BasePageButtonElement(BasePageElement, metaclass=ABCMeta):
    """Base Page Element for all UI button elements"""

    @retry_on_selenium_error()
    def submit(self) -> None:
        """Submit current button element on the page"""
        WebDriverWait(self._driver, 100).until(lambda driver: driver.find_element(*self.locator))
        element = self._driver.find_element(*self.locator)
        element.submit()
