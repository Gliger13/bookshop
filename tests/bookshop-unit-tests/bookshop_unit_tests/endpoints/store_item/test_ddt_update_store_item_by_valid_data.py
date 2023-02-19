"""Data Driven Unit Test to check PUT /api/store-item/{store_item_id} endpoint"""
import pytest
from aiohttp import BasicAuth
from flask import Flask
from requests import codes

from bookshop_test_framework.asserts.unit.response import SimpleResponse, soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_ddt_update_store_item_by_valid_data(test_data: dict, application_client: Flask):
    """Test PUT /api/store-item/{store_item_id} endpoint

    :param test_data: current test set data
    :param application_client: bookshop testing application
    """
    store_item_id_to_update = test_data.get("store_item_id_to_update")
    endpoint = f"/api/store-item/{store_item_id_to_update}"
    new_store_item_attributes = test_data.get("new_store_item_attributes", {})
    response = application_client.put(
        endpoint,
        json=new_store_item_attributes,
        auth=BasicAuth(**test_data["actor_credentials"])
    )
    soft_check_response_status_code(SimpleResponse(endpoint, "PUT", response.status_code), codes.ok)
