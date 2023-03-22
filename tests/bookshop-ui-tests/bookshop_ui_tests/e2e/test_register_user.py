"""Smoke UI E2E test to check user registration"""
import pytest
from faker import Faker

from bookshop_test_framework.config.config import BookshopUiEndpoints, Config
from bookshop_test_framework.tools.data_generator.test_data_generator import TestDataGenerator
from bookshop_test_framework.tools.pages.user.pages import RegistrationPage
from bookshop_test_framework.tools.soft_assert.soft_assert import expect
from bookshop_test_framework.tools.test_data import get_parametrized_test_data, get_test_data_ids
from bookshop_test_framework.tools.test_results.ui_test_results import UiTestResult


@pytest.mark.smoke
@pytest.mark.e2e
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
def test_register_user(test_data: dict, config: Config, registration_page: RegistrationPage, faker: Faker) -> None:
    """Test user can be registered via UI registration page

    :param test_data: test data for the current test
    :param config: test config for the current environment
    :param registration_page: page object for registration page
    :param faker: initialized fake data generator
    """
    user_login = TestDataGenerator.generate_valid_test_login()
    registration_page.login_input_element.set(TestDataGenerator.generate_valid_test_login())
    registration_page.password_input_element.set(TestDataGenerator.generate_valid_password())
    registration_page.email_input_element.set(TestDataGenerator.generate_valid_test_email(user_login))
    registration_page.phone_input_element.set(f"+{faker.msisdn()[3:]}")
    registration_page.name_input_element.set(faker.name())
    registration_page.address_input_element.set(faker.address())
    registration_page.click_submit_button()

    products_page_url = f"{config.base_url}/{BookshopUiEndpoints.REGISTRATION_PAGE}"
    expect(
        registration_page.is_registration_success(products_page_url),
        UiTestResult(
            check_message="Check registration page redirects to the products page after success registration",
            endpoint=BookshopUiEndpoints.REGISTRATION_PAGE,
        ),
    )
