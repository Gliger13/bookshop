"""Data Driven Unit Test to check PUT /api/booking/{booking_id} endpoint"""
import pytest
from aiohttp import BasicAuth
from flask import Flask
from requests import codes

from bookshop_test_framework.asserts.unit.response import SimpleResponse
from bookshop_test_framework.asserts.unit.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data
from bookshop_test_framework.tools.test_data import get_test_data_ids


@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_ddt_update_booking_by_valid_data(test_data: dict, application_client: Flask):
    """Test PUT /api/booking/{booking_id} endpoint

    :param test_data: current test set data
    :param application_client: bookshop testing application
    """
    booking_id_to_update = test_data.get("booking_id_to_update")
    endpoint = f"/api/booking/{booking_id_to_update}"
    new_booking_attributes = test_data.get("new_booking_attributes", {})
    token_response = application_client.get("/api/generate_token", auth=BasicAuth(**test_data["actor_credentials"]))
    response = application_client.put(
        endpoint, json=new_booking_attributes, headers={"Authorization": f"Bearer {token_response.json['AuthToken']}"}
    )
    soft_check_response_status_code(SimpleResponse(endpoint, "PUT", response.status_code), codes.ok)
