"""User page locators"""
from selenium.webdriver.common.by import By

from .._base.locators import BasePageLocators
from .._base.locators import Locator


class RegistrationPageLocators(BasePageLocators):
    """Locators for user registration page"""

    LOGIN_INPUT = Locator(By.ID, "login")
    PASSWORD_INPUT = Locator(By.ID, "password")
    EMAIL_INPUT = Locator(By.ID, "email")
    PHONE_INPUT = Locator(By.ID, "phone")
    NAME_INPUT = Locator(By.ID, "name")
    ADDRESS_INPUT = Locator(By.ID, "address")
    SUBMIT_FORM_BUTTON = Locator(By.ID, "submit")


class ProfilePageLocators(BasePageLocators):
    """Locators for profile page"""

    DELETE_PROFILE_BUTTON = Locator(By.ID, "delete_user_button")
