"""Test Data based application fixtures

Module contains fixtures that produces application models using data from the
current test set.
"""
import pytest

from bookshop_app.models.booking import BookingModel
from bookshop_app.models.product import ProductModel
from bookshop_app.models.store_item import StoreItemModel
from bookshop_app.models.user import UserModel
from bookshop_app.schemas.booking import BookingSchema
from bookshop_app.schemas.product import ProductSchema
from bookshop_app.schemas.store_item import StoreItemSchema
from bookshop_app.schemas.user import UserSchema
from bookshop_test_framework.mocks.dao.booking_status import FakeBookingStatusDAO
from bookshop_test_framework.mocks.dao.role import FakeRoleDAO


@pytest.fixture
def test_data_user_models(test_data: dict) -> list[UserModel]:
    """Generate and return user models using given test data

    :param test_data: dict with current test set data
    :return: user models
    """
    user_models: list[UserModel] = []
    user_schema = UserSchema()
    for user_id, test_data_user_model in enumerate(test_data.get("mock_user_models", [])):
        user_password = test_data_user_model.pop("password", "Welcome1")
        user_model = user_schema.load(test_data_user_model)
        user_model.hash_password(user_password)
        user_model.role = FakeRoleDAO.get_by_id(user_model.role_id)
        user_model.id = user_id + 1
        user_models.append(user_model)
    return user_models


@pytest.fixture
def test_data_product_models(test_data: dict) -> list[ProductModel]:
    """Generate and return product models using given test data

    :param test_data: dict with current test set data
    :return: product models
    """
    product_models: list[ProductModel] = []
    product_schema = ProductSchema()
    for product_id, test_data_product_model in enumerate(test_data.get("mock_product_models", [])):
        product_model = product_schema.load(test_data_product_model)
        product_model.id = product_id + 1
        product_models.append(product_model)
    return product_models


@pytest.fixture
def test_data_booking_models(test_data: dict) -> list[BookingModel]:
    """Generate and return booking models using given test data

    :param test_data: dict with current test set data
    :return: booking models
    """
    booking_models: list[BookingModel] = []
    booking_schema = BookingSchema()
    for booking_id, test_data_booking_model in enumerate(test_data.get("mock_booking_models", [])):
        booking_model = booking_schema.load(test_data_booking_model)
        booking_model.id = booking_id + 1
        booking_model.status = FakeBookingStatusDAO.get_by_id(booking_model.status_id)
        booking_models.append(booking_model)
    return booking_models


@pytest.fixture
def test_data_store_item_models(test_data: dict) -> list[StoreItemModel]:
    """Generate and return store item models using given test data

    :param test_data: dict with current test set data
    :return: store item models
    """
    store_item_models: list[StoreItemModel] = []
    store_item_schema = StoreItemSchema()
    for store_item_id, test_data_store_item_model in enumerate(test_data.get("mock_store_item_models", [])):
        store_item_model = store_item_schema.load(test_data_store_item_model)
        store_item_model.id = store_item_id + 1
        store_item_models.append(store_item_model)
    return store_item_models
