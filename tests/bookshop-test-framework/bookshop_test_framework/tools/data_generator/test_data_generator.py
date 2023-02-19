"""Test data generator

Module contains generator that generates unique and secure test data for tests.
"""
import string
from datetime import datetime
from random import choice

from bookshop_test_framework.models.booking import Booking
from bookshop_test_framework.models.product import Product
from bookshop_test_framework.models.store_item import StoreItem
from bookshop_test_framework.models.user import User


class TestDataGenerator:
    """Provides methods to generate different user data"""

    @staticmethod
    def generate_valid_password() -> str:
        """Generate and return strong valid password"""
        password_length = 64
        characters = *string.ascii_letters, *string.digits, *string.punctuation
        return "".join(choice(characters) for _ in range(password_length))

    @staticmethod
    def generate_valid_test_login() -> str:
        """Generate and return strong unique login"""
        login_length = 8
        characters = *string.ascii_letters, *string.digits
        random_part = "".join(choice(characters) for _ in range(login_length))
        return f"TestUser_{datetime.now().strftime('%H-%M-%S_%d-%m-%Y')}_{random_part}"

    @staticmethod
    def generate_valid_test_email(test_login: str) -> str:
        """Return valid test email based on the given login

        :param test_login: unique valid login for generating email
        :return: valid test email based on provided login
        """
        return f"{test_login}@mail.com"

    @staticmethod
    def generate_basic_user() -> User:
        """Generate and return user with generated fields"""
        user = User()
        user.login = TestDataGenerator.generate_valid_test_login()
        user.password = TestDataGenerator.generate_valid_password()
        user.email = TestDataGenerator.generate_valid_test_email(user.login)
        user.address = "Test Country, Test City, Test District, Test Home Number, 00-000000"
        user.role_id = 3
        return user

    @staticmethod
    def generate_basic_product() -> Product:
        """Generate and return basic product model"""
        product = Product()
        product.name = "Testing Book"
        product.description = "Book for testing"
        product.author = "Test Author"
        product.price = 999.99
        return product

    @staticmethod
    def generate_basic_booking() -> Booking:
        """Generate and return basic booking model"""
        booking = Booking()
        booking.quantity = 1
        return booking

    @staticmethod
    def generate_basic_store_item() -> StoreItem:
        """Generate and return basic store item model"""
        store_item = StoreItem()
        store_item.available_quantity = 50
        return store_item
