"""Mocked Data Access Object fixture

Module contains fixtures that provides prepared fake data access objects for
different application models.
"""
from typing import Iterable

import pytest

from bookshop_app.models.booking import BookingModel
from bookshop_app.models.product import ProductModel
from bookshop_app.models.store_item import StoreItemModel
from bookshop_app.models.user import UserModel
from bookshop_test_framework.mocks.dao.booking import FakeBookingDAO
from bookshop_test_framework.mocks.dao.product import FakeProductDAO
from bookshop_test_framework.mocks.dao.store_item import FakeStoreItemDAO
from bookshop_test_framework.mocks.dao.user import FakeUserDAO

__all__ = [
    "mocked_booking_dao",
    "mocked_product_dao",
    "mocked_store_item_dao",
    "mocked_user_dao",
]


@pytest.fixture
def mocked_user_dao(test_data_user_models: Iterable[UserModel]) -> type[FakeUserDAO]:
    """Prepare and return mocked user DAO type

    :param test_data_user_models: iterable of user models to add to DAO
    :return: prepared mocked DAO
    """
    for model in test_data_user_models:
        FakeUserDAO.create(model)
    return FakeUserDAO


@pytest.fixture
def mocked_product_dao(test_data_product_models: Iterable[ProductModel]) -> type[FakeProductDAO]:
    """Prepare and return mocked product DAO type

    :param test_data_product_models: iterable of product models to add to DAO
    :return: prepared mocked DAO
    """
    for model in test_data_product_models:
        FakeProductDAO.create(model)
    return FakeProductDAO


@pytest.fixture
def mocked_booking_dao(test_data_booking_models: Iterable[BookingModel]) -> type[FakeBookingDAO]:
    """Prepare and return mocked booking DAO type

    :param test_data_booking_models: iterable of booking models to add to DAO
    :return: prepared mocked DAO
    """
    for model in test_data_booking_models:
        FakeBookingDAO.create(model)
    return FakeBookingDAO


@pytest.fixture
def mocked_store_item_dao(test_data_store_item_models: Iterable[StoreItemModel]) -> type[FakeStoreItemDAO]:
    """Prepare and return mocked store item DAO type

    :param test_data_store_item_models: iterable of store item models to add
    :return: prepared mocked DAO
    """
    for model in test_data_store_item_models:
        FakeStoreItemDAO.create(model)
    return FakeStoreItemDAO
