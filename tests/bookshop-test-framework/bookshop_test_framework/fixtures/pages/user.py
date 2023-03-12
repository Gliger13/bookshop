"""User pages fixtures

Module contains fixtures that provide page objects for interacting with user UI
pages using selenium.
"""
import pytest
from selenium.webdriver.firefox.webdriver import WebDriver

from bookshop_test_framework.config.config import BookshopUiEndpoints, Config
from bookshop_test_framework.tools.pages.user.pages import RegistrationPage

__all__ = ["registration_page"]


@pytest.fixture
def registration_page(driver: WebDriver, config: Config) -> RegistrationPage:
    """Get registration page object

    :param driver: initialized selenium driver for interactions with the page
    :param config: test config for the current environment
    :return: initialized registration page object
    """
    registration_page_url = f"{config.base_url}/{BookshopUiEndpoints.REGISTRATION_PAGE}"
    driver.get(registration_page_url)
    return RegistrationPage(driver)
