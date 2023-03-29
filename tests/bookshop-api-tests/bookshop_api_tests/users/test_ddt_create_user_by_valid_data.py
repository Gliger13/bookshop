"""Data Driven Test to check user creation with valid data"""
import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.asserts.api.user import check_create_user_response
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.test_data import get_parametrized_test_data
from bookshop_test_framework.tools.test_data import get_test_data_ids


@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_create_user_by_valid_data(
    test_data: dict, created_user_response: ClientResponse, generated_user: User
):
    """Data Driven Test to create user by valid data

    :param test_data: dict with current test set data
    :param created_user_response: create user response to check
    """
    await check_create_user_response(created_user_response, generated_user)
