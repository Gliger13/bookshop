"""Data Driven Unit Test to check GET /api/product endpoint"""
import pytest
from flask import Flask
from requests import codes

from bookshop_test_framework.asserts.unit.response import SimpleResponse
from bookshop_test_framework.asserts.unit.response import soft_check_response_status_code
from bookshop_test_framework.tools.test_data import get_parametrized_test_data
from bookshop_test_framework.tools.test_data import get_test_data_ids


@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_ddt_get_all_products(test_data: dict, application_client: Flask):
    """Test GET /api/product endpoint

    :param test_data: current test set data
    :param application_client: bookshop testing application
    """
    endpoint = "/api/product"
    response = application_client.get(endpoint)
    soft_check_response_status_code(SimpleResponse(endpoint, "GET", response.status_code), codes.ok)
