"""Smoke test to check update product"""
import pytest
from aiohttp import ClientResponse
from requests import codes

from bookshop_test_framework.asserts.api.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data
from bookshop_test_framework.tools.test_data import get_test_data_ids


@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_smoke_update_product(test_data: dict, session_update_product_response: ClientResponse):
    """Smoke test to update product

    :param test_data: dict with current test set data
    :param session_update_product_response: update product response to check
    """
    soft_check_response_status_code(session_update_product_response, codes.ok)
