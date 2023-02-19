"""Mock for user data access object class

Module provides auto-use fixture that mocks user data access object class.
"""
from inspect import getmembers
from unittest.mock import patch

import pytest

from bookshop_test_framework.mocks.dao.booking import FakeBookingDAO
from bookshop_test_framework.mocks.dao.booking_status import FakeBookingStatusDAO
from bookshop_test_framework.mocks.dao.product import FakeProductDAO
from bookshop_test_framework.mocks.dao.role import FakeRoleDAO
from bookshop_test_framework.mocks.dao.store_item import FakeStoreItemDAO
from bookshop_test_framework.mocks.dao.user import FakeUserDAO

__all__ = ["dao_patch"]


def _patch_by_class(class_reference: str, mocked_class: type) -> list:
    """Patch given class with the attributes of the given fake class

    :param class_reference: class reference to patch with mocked
    :param mocked_class: mocked class to set
    :return:
    """
    mocks: list = []
    fake_class_attribute_names = getmembers(mocked_class)
    for class_attribute in fake_class_attribute_names:
        attribute_name, attribute_value = class_attribute
        if not attribute_name.startswith("__") and not attribute_name.startswith("_"):
            mocks.append(patch(f"{class_reference}.{attribute_name}", attribute_value))
    return mocks


@pytest.fixture(autouse=True)
def dao_patch(mocked_booking_dao: type[FakeBookingDAO], mocked_product_dao: type[FakeProductDAO],
              mocked_store_item_dao: type[FakeStoreItemDAO], mocked_user_dao: type[FakeUserDAO]) -> None:
    """Patches all Data Access Objects with mocked one

    :param mocked_booking_dao: mocked booking data access object class
    :param mocked_product_dao: mocked product data access object class
    :param mocked_store_item_dao: mocked store item data access object class
    :param mocked_user_dao: mocked user data access object class
    """
    dao_package_reference = "bookshop_app.data_access_objects"
    patches = [
        *_patch_by_class(f"{dao_package_reference}.user.UserDAO", mocked_user_dao),
        *_patch_by_class(f"{dao_package_reference}.product.ProductDAO", mocked_product_dao),
        *_patch_by_class(f"{dao_package_reference}.booking.BookingDAO", mocked_booking_dao),
        *_patch_by_class(f"{dao_package_reference}.store_item.StoreItemDAO", mocked_store_item_dao),
        *_patch_by_class(f"{dao_package_reference}.booking_status.BookingStatusDAO", FakeBookingStatusDAO),
        *_patch_by_class(f"{dao_package_reference}.role.RoleDAO", FakeRoleDAO),
    ]
    for dao_patch in patches:
        dao_patch.start()

    yield

    for dao_patch in patches:
        dao_patch.stop()
