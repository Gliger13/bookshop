"""Store item managing fixtures

Module contains fixtures for creating, deleting, getting store items in
different testing scopes.
"""
from asyncio import TaskGroup
from typing import Optional

import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.models.product import Product
from bookshop_test_framework.models.store_item import StoreItem
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import StoreItemApi, UserApi
from bookshop_test_framework.tools.data_generator.test_data_generator import TestDataGenerator


@pytest.fixture(scope="session")
async def session_store_item(store_items_api: StoreItemApi, users_api: UserApi, session_product: Product,
                             session_manager_user: User, http_task_group: TaskGroup) -> Product:
    """Generate, create and return store item in session scope

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param session_product: generated and created product in the session scope
    :param session_manager_user: manager user to use for authentication
    :param http_task_group: async task group for executing http requests
    :return: created store item
    """
    store_item = TestDataGenerator.generate_basic_store_item()
    store_item.product_id = session_product.id
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    create_store_item_response = await store_items_api.create(store_item, headers=authentication_headers)
    assert create_store_item_response.ok, "Failed to create session store item.\n" \
                                          f"Request status code: {create_store_item_response.status}\n" \
                                          f"Response message: {await create_store_item_response.text()}"

    create_store_item_response_json = await create_store_item_response.json()
    store_item.id = create_store_item_response_json["id"]

    yield store_item

    http_task_group.create_task(store_items_api.delete(store_item.id, headers=authentication_headers))


@pytest.fixture(scope="session")
async def session_get_store_item_response(store_items_api: StoreItemApi, users_api: UserApi, session_manager_user: User,
                                          session_store_item: StoreItem) -> ClientResponse:
    """Get session store item wit session manager and return response

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :param session_store_item: created store item in the session scope
    :return: get store item response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await store_items_api.get(session_store_item.id, headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_get_all_store_items_response(store_items_api: StoreItemApi, users_api: UserApi,
                                               session_manager_user: User) -> ClientResponse:
    """Send request to get all store items and return response

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :return: get all store items response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await store_items_api.get_all(headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_update_store_item_response(store_items_api: StoreItemApi, users_api: UserApi,
                                             session_manager_user: User,
                                             session_store_item: StoreItem) -> ClientResponse:
    """Send request to update given store item and return response

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :param session_store_item: created store item to update
    :return: update store item response
    """
    attributes_to_update = {"booked_quantity": 2}
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await store_items_api.update(session_store_item.id, attributes_to_update, headers=authentication_headers)


@pytest.fixture
async def created_store_item_response(store_items_api: StoreItemApi, users_api: UserApi,
                                      generated_store_item: StoreItem, session_manager_user: User,
                                      http_task_group: TaskGroup) -> ClientResponse:
    """Create generated store item and return response

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param generated_store_item: generated store item
    :param session_manager_user: manager user model
    :param http_task_group: async task group for executing http requests
    :return: create store item response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    create_store_item_response = await store_items_api.create(generated_store_item, headers=authentication_headers)

    yield create_store_item_response

    if create_store_item_response.ok:
        create_store_item_response_json = await create_store_item_response.json()
        created_store_item_id = create_store_item_response_json["id"]
        http_task_group.create_task(store_items_api.delete(created_store_item_id, headers=authentication_headers))


@pytest.fixture
async def created_store_item(created_store_item_response: ClientResponse,
                             generated_store_item: StoreItem) -> Optional[StoreItem]:
    """Create generated store item and return created store item model

    :param created_store_item_response: response to create generated store item
    :param generated_store_item: generated store item
    :return: generated and created store item model
    """
    if created_store_item_response.ok:
        created_store_item_response_json = await created_store_item_response.json()
        generated_store_item.id = created_store_item_response_json["id"]
        return generated_store_item
    return None


@pytest.fixture
async def deleted_store_item_response(store_items_api: StoreItemApi, users_api: UserApi,
                                      generated_store_item: StoreItem, session_admin_user: User) -> ClientResponse:
    """Delete generated and created store item and return response

    :param store_items_api: initialized StoreItem API
    :param users_api: initialized User API
    :param generated_store_item: generated and created store item model
    :param session_admin_user: manager user model
    :return: delete created store item response
    """
    authentication_headers = await users_api.get_auth_header(session_admin_user)
    create_store_item_response = await store_items_api.create(generated_store_item, headers=authentication_headers)
    assert create_store_item_response.ok, "Failed to create store item to delete later.\n" \
                                          f"Request status code: {create_store_item_response.status}\n" \
                                          f"Response message: {await create_store_item_response.text()}"

    create_store_item_response_json = await create_store_item_response.json()
    created_store_item_id = create_store_item_response_json["id"]
    return await store_items_api.delete(created_store_item_id, headers=authentication_headers)
