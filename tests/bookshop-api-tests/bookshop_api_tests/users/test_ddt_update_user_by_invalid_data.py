"""Data Driven Test to check user updating with invalid data"""
import pytest
from aiohttp import ClientResponse
from requests import codes

from bookshop_test_framework.asserts.api.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_update_user_by_invalid_data(test_data: dict, updated_user_response: ClientResponse):
    """Data Driven Test to update user by invalid data

    :param test_data: dict with current test set data
    :param updated_user_response: update user response to check
    """
    soft_check_response_status_code(updated_user_response, codes.bad_request)
