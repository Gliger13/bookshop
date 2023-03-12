"""Selenium web driver fixtures"""
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

__all__ = ["driver"]


@pytest.fixture
def driver() -> WebDriver:
    """Initialize, configure and return selenium web driver"""
    options = Options()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)
