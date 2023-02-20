"""Data Driven Unit Test to check GET /api/store-item/{store_item_id} endpoint"""
import pytest
from aiohttp import BasicAuth
from flask import Flask
from requests import codes

from bookshop_test_framework.asserts.unit.response import SimpleResponse, soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_ddt_get_valid_store_item(test_data: dict, application_client: Flask):
    """Test GET /api/store-item/{store_item_id} endpoint

    :param test_data: current test set data
    :param application_client: bookshop testing application
    """
    store_item_id_to_get = test_data["store_item_id_to_get"]
    endpoint = f"/api/store-item/{store_item_id_to_get}"
    response = application_client.get(endpoint, auth=BasicAuth(**test_data["actor_credentials"]))
    soft_check_response_status_code(SimpleResponse(endpoint, "GET", response.status_code), codes.ok)
