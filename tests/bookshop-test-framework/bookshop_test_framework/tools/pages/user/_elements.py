"""User page elements"""
from functools import cached_property

from ._locators import ProfilePageLocators, RegistrationPageLocators
from .._base.elements import BasePageButtonElement, BasePageElement
from .._base.locators import Locator


class LoginInputElement(BasePageElement):
    """Registration page login input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for login input"""
        return RegistrationPageLocators.LOGIN_INPUT


class PasswordInputElement(BasePageElement):
    """Registration page password input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for password input"""
        return RegistrationPageLocators.PASSWORD_INPUT


class EmailInputElement(BasePageElement):
    """Registration page email input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for email input"""
        return RegistrationPageLocators.EMAIL_INPUT


class PhoneInputElement(BasePageElement):
    """Registration page phone input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for phone input"""
        return RegistrationPageLocators.PHONE_INPUT


class NameInputElement(BasePageElement):
    """Registration page name input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for name input"""
        return RegistrationPageLocators.NAME_INPUT


class AddressInputElement(BasePageElement):
    """Registration page address input element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for address input"""
        return RegistrationPageLocators.ADDRESS_INPUT


class SubmitButtonElement(BasePageButtonElement):
    """Registration page submit button element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for submit button"""
        return RegistrationPageLocators.SUBMIT_FORM_BUTTON


class DeleteUserSubmitButtonElement(BasePageButtonElement):
    """Registration page delete user button element"""

    @cached_property
    def locator(self) -> Locator:
        """Return element locator for delete user button"""
        return ProfilePageLocators.DELETE_PROFILE_BUTTON
