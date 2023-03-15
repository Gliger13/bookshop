"""Selenium web driver fixtures"""
import os

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
    if web_driver_url := os.getenv("REMOTE_WEB_DRIVER_URL"):
        driver = webdriver.Remote(options=options, command_executor=web_driver_url)
    else:
        driver = webdriver.Firefox(options=options)

    yield driver

    driver.quit()
