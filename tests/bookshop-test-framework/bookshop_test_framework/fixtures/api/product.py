"""Product managing fixtures

Module contains fixtures for creating, deleting, getting products in different
testing scopes.
"""
from asyncio import TaskGroup
from typing import Optional

import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.models.product import Product
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import ProductApi, UserApi
from bookshop_test_framework.tools.data_generator.test_data_generator import TestDataGenerator


@pytest.fixture(scope="session")
async def session_product(products_api: ProductApi, users_api: UserApi, session_manager_user: User,
                          http_task_group: TaskGroup) -> Product:
    """Generate, create and return customer user in session scope

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :param http_task_group: async task group for executing http requests
    :return: created product
    """
    product = TestDataGenerator.generate_basic_product()
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    create_product_response = await products_api.create(product, headers=authentication_headers)
    assert create_product_response.ok, "Failed to create session product.\n" \
                                       f"Request status code: {create_product_response.status}\n" \
                                       f"Response message: {await create_product_response.text()}"

    create_product_response_json = await create_product_response.json()
    product.id = create_product_response_json["id"]

    yield product

    http_task_group.create_task(products_api.delete(product.id, headers=authentication_headers))


@pytest.fixture(scope="session")
async def session_get_product_response(products_api: ProductApi, users_api: UserApi, session_customer_user: User,
                                       session_product: Product) -> ClientResponse:
    """Get session product with session customer user and return response

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param session_customer_user: customer user to use for authentication
    :param session_product: created product in the session scope
    :return: get product response
    """
    authentication_headers = await users_api.get_auth_header(session_customer_user)
    return await products_api.get(session_product.id, headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_get_all_products_response(products_api: ProductApi, users_api: UserApi,
                                            session_customer_user: User) -> ClientResponse:
    """Send request to get all products and return response

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param session_customer_user: customer user to use for authentication
    :return: get all products response
    """
    authentication_headers = await users_api.get_auth_header(session_customer_user)
    return await products_api.get_all(headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_update_product_response(products_api: ProductApi, users_api: UserApi, session_manager_user: User,
                                          session_product: Product) -> ClientResponse:
    """Send request to update given product and return response

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :param session_product: created product to update
    :return: update product response
    """
    product_attributes_to_update = {"description": "new test book description"}
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await products_api.update(session_product.id, product_attributes_to_update, headers=authentication_headers)


@pytest.fixture
async def created_product_response(products_api: ProductApi, users_api: UserApi, generated_product: Product,
                                   session_manager_user: User, http_task_group: TaskGroup) -> ClientResponse:
    """Create generated product and return response

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param generated_product: generated product
    :param session_manager_user: manager user model
    :param http_task_group: async task group for executing http requests
    :return: create product response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    create_product_response = await products_api.create(generated_product, headers=authentication_headers)

    yield create_product_response

    if create_product_response.ok:
        create_product_response_json = await create_product_response.json()
        created_product_id = create_product_response_json["id"]
        http_task_group.create_task(products_api.delete(created_product_id, headers=authentication_headers))


@pytest.fixture
async def created_product(created_product_response: ClientResponse, generated_product: Product) -> Optional[Product]:
    """Create generated product and return generated product model

    :param created_product_response: response to create generated product
    :param generated_product: generated product
    :return: generated and created product model
    """
    if created_product_response.ok:
        created_product_response_json = await created_product_response.json()
        generated_product.id = created_product_response_json["id"]
        return generated_product
    return None


@pytest.fixture
async def deleted_product_response(products_api: ProductApi, users_api: UserApi, generated_product: Product,
                                   session_manager_user: User) -> ClientResponse:
    """Delete generated and created product and return response

    :param products_api: initialized Product API
    :param users_api: initialized User API
    :param generated_product: generated product
    :param session_manager_user: manager user model
    :return: delete created product response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    create_product_response = await products_api.create(generated_product, headers=authentication_headers)
    assert create_product_response.ok, "Failed to create product to delete later.\n" \
                                       f"Request status code: {create_product_response.status}\n" \
                                       f"Response message: {await create_product_response.text()}"

    create_product_response_json = await create_product_response.json()
    create_product_id = create_product_response_json["id"]
    return await products_api.delete(create_product_id, headers=authentication_headers)
