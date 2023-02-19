"""Smoke test to check get all bookings"""
import pytest
from aiohttp import ClientResponse
from requests import codes

from bookshop_test_framework.asserts.api.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_smoke_get_all_bookings(test_data: dict, session_get_all_bookings_response: ClientResponse):
    """Smoke test to get all bookings

    :param test_data: dict with current test set data
    :param session_get_all_bookings_response: get all bookings response to check
    """
    soft_check_response_status_code(session_get_all_bookings_response, codes.ok)
