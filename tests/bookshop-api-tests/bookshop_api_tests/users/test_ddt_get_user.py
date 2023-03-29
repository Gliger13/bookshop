"""Data Driven Test to check get user endpoint"""
import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.asserts.api.user import check_get_user_response
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import UserApi
from bookshop_test_framework.tools.test_data import get_parametrized_test_data
from bookshop_test_framework.tools.test_data import get_test_data_ids


@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_get_user(
    test_data: dict, users_api: UserApi, customer_user: User, get_customer_user_response: ClientResponse
):
    """Data Driven Test to get user

    :param test_data: dict with current test set data
    :param get_customer_user_response: get user response to check
    """
    await check_get_user_response(get_customer_user_response, customer_user)
