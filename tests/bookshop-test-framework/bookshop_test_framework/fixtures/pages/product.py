"""Product pages fixtures

Module contains fixtures that provide page objects for interacting with product
UI pages using selenium.
"""
import pytest
from selenium.webdriver.firefox.webdriver import WebDriver

from bookshop_test_framework.config.config import BookshopUiEndpoints, Config
from bookshop_test_framework.tools.pages.user.pages import ProductsPage

__all__ = ["products_page"]


@pytest.fixture
def products_page(driver: WebDriver, config: Config) -> ProductsPage:
    """Get products page object

    :param driver: initialized selenium driver for interactions with the page
    :param config: test config for the current environment
    :return: initialized products page object
    """
    products_page_url = f"{config.base_url}/{BookshopUiEndpoints.PRODUCTS_PAGE}"
    driver.get(products_page_url)
    return ProductsPage(driver)
