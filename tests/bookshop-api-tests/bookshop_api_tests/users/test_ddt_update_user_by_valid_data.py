"""Data Driven Test to check user updating with valid data"""
import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.asserts.api.user import check_update_user_response
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import UserApi
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_update_user_by_valid_data(
    test_data: dict, users_api: UserApi, customer_user: User, updated_user_response: ClientResponse
):
    """Data Driven Test to update user by valid data

    :param test_data: dict with current test set data
    :param updated_user_response: update user response to check
    """
    await check_update_user_response(updated_user_response, customer_user)
