"""Data Driven Unit Test to check DELETE /api/product/{product_id} endpoint"""
import pytest
from aiohttp import BasicAuth
from flask import Flask
from requests import codes

from bookshop_test_framework.asserts.unit.response import SimpleResponse, soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids


@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_ddt_delete_valid_product(test_data: dict, application_client: Flask):
    """Test DELETE /api/product/{product_id} endpoint

    :param test_data: current test set data
    :param application_client: bookshop testing application
    """
    product_id_to_delete = test_data["product_id_to_delete"]
    endpoint = f"/api/product/{product_id_to_delete}"
    token_response = application_client.get("/api/generate_token", auth=BasicAuth(**test_data["actor_credentials"]))
    response = application_client.delete(
        endpoint, headers={"Authorization": f"Bearer {token_response.json['AuthToken']}"}
    )
    soft_check_response_status_code(SimpleResponse(endpoint, "DELETE", response.status_code), codes.ok)
