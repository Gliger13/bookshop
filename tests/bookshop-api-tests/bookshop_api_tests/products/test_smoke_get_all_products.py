"""Smoke test to check get all products"""
import pytest
from aiohttp import ClientResponse
from requests import codes

from bookshop_test_framework.asserts.api.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_smoke_get_all_products(test_data: dict, session_get_all_products_response: ClientResponse):
    """Smoke test to get all products

    :param test_data: dict with current test set data
    :param session_get_all_products_response: get all products response to check
    """
    soft_check_response_status_code(session_get_all_products_response, codes.ok)