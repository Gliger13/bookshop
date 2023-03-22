"""User page objects"""
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from ._elements import (
    AddressInputElement,
    EmailInputElement,
    LoginInputElement,
    NameInputElement,
    PasswordInputElement,
    PhoneInputElement,
    SubmitButtonElement,
)
from .._base.pages import BasePage


class RegistrationPage(BasePage):
    """Registration page object

    Object responsible for interacting with the registration ui page using
    given selenium driver.
    """

    __slots__ = [
        "login_input_element",
        "password_input_element",
        "email_input_element",
        "phone_input_element",
        "name_input_element",
        "address_input_element",
        "submit_button_element",
    ]

    def __init__(self, driver: WebDriver) -> None:
        """Initialize page object with the given driver

        :param driver: selenium driver to use for ui interactions
        """
        super().__init__(driver)
        self.login_input_element = LoginInputElement(self._driver)
        self.password_input_element = PasswordInputElement(self._driver)
        self.email_input_element = EmailInputElement(self._driver)
        self.phone_input_element = PhoneInputElement(self._driver)
        self.name_input_element = NameInputElement(self._driver)
        self.address_input_element = AddressInputElement(self._driver)
        self.submit_button_element = SubmitButtonElement(self._driver)

    def click_submit_button(self) -> None:
        """Click registration page submit button element"""
        self.submit_button_element.submit()

    def is_registration_success(self, after_success_registration_url: str) -> bool:
        """Return True if the registration request was success else False

        Return True if the URL of the current page was switched to the URL of
        the given product's page, indicating the success of the registration
        process. If the page is the same - registration failed, return False.

        :param after_success_registration_url: expected url after success
            registration
        :return: True if the user registration was success else False
        """
        try:
            wait = WebDriverWait(self._driver, timeout=5)
            wait.until(lambda driver: driver.current_url == after_success_registration_url)
            return True
        except TimeoutException:
            return False


class ProductsPage(BasePage):
    """Products page object

    Object responsible for interacting with the products ui page using given
    selenium driver.
    """

    __slots__ = []

    def __init__(self, driver: WebDriver) -> None:
        """Initialize page object with the given driver

        :param driver: selenium driver to use for ui interactions
        """
        super().__init__(driver)

    def get_page_title(self) -> str:
        """Return current ui page title"""
        return self._driver.title
