"""Generated models

Module provides fixtures for generating different data models for tests.
"""
import pytest

from bookshop_test_framework.config.config import Config
from bookshop_test_framework.models.booking import Booking
from bookshop_test_framework.models.product import Product
from bookshop_test_framework.models.store_item import StoreItem
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.data_generator.test_data_generator import TestDataGenerator


@pytest.fixture
def generated_user(test_data: dict, config: Config) -> User:
    """Generate and return user using test data

    :param test_data: current test set data
    :param config: current environment config
    :return: generated user model
    """
    user = TestDataGenerator.generate_basic_user()
    test_data_user_attributes = test_data.get("user", {})
    user.update(test_data_user_attributes)
    return user


@pytest.fixture
def generated_product(test_data: dict, config: Config) -> Product:
    """Generate and return product using test data

    :param test_data: current test set data
    :param config: current environment config
    :return: generated product model
    """
    product = TestDataGenerator.generate_basic_product()
    test_data_product_attributes = test_data.get("product", {})
    product.update(test_data_product_attributes)
    return product


@pytest.fixture
def generated_booking(test_data: dict, created_product: Product, customer_user: User) -> Booking:
    """Generate and return booking model using test data

    :param test_data: current test set data
    :param created_product: generated and created product for the booking
    :param customer_user: generated and created user for the booking
    :return: generated booking model
    """
    booking = TestDataGenerator.generate_basic_booking()
    test_data_booking_attributes = test_data.get("booking", {})
    booking.update({
        "product_id": created_product.id,
        "user_id": customer_user.id,
        "delivery_address": customer_user.address,
        **test_data_booking_attributes
    })
    return booking


@pytest.fixture
def generated_store_item(test_data: dict, created_product: Product) -> StoreItem:
    """Generate and return store item model using test data

    :param test_data: current test set data
    :param created_product: generated and created product for the store item
    :return: generated store item model
    """
    store_item = TestDataGenerator.generate_basic_store_item()
    test_data_store_item_attributes = test_data.get("store_item", {})
    store_item.update({
        "product_id": created_product.id,
        **test_data_store_item_attributes
    })
    return store_item
