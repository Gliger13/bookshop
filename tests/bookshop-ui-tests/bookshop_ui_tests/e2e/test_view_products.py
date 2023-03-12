"""Smoke UI E2E test to check products view"""
import pytest

from bookshop_test_framework.config.config import BookshopUiEndpoints
from bookshop_test_framework.tools.pages.user.pages import ProductsPage
from bookshop_test_framework.tools.soft_assert.soft_assert import expect
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids
from bookshop_test_framework.tools.test_results.ui_test_results import UiTestResult


@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_view_products(test_data: dict, products_page: ProductsPage) -> None:
    """Test view products page

    Get products page UI and check if the page title is the same as the
    products page has.

    :param test_data: data for the current test case
    :param products_page: page object for products page
    """
    actual_product_page_title = products_page.get_page_title()
    expected_products_page_title = test_data["expected_products_page_title"]
    expect(actual_product_page_title == expected_products_page_title, UiTestResult(
        check_message="Check products page has correct title",
        endpoint=BookshopUiEndpoints.REGISTRATION_PAGE,
        actual_result=actual_product_page_title,
        expected_result=expected_products_page_title
    ))
