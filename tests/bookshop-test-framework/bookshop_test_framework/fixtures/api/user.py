"""User API related fixtures

Module contains fixtures that manages users using User API. Provides users with
different user attributes or user creating scope. Responsible for creating,
updating, getting, deleting users.
"""
import logging
from asyncio import TaskGroup
from dataclasses import asdict
from json import JSONDecodeError

import pytest
from aiohttp import ClientResponse, ContentTypeError

from bookshop_test_framework.config.config import Config
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import UserApi
from bookshop_test_framework.tools.data_generator.test_data_generator import TestDataGenerator


@pytest.fixture(scope="session")
async def session_customer_user(config: Config, users_api: UserApi, http_task_group: TaskGroup) -> User:
    """Generate, create and return customer user in session scope

    :param config: current test environment config
    :param users_api: initialized User API
    :param http_task_group: async task group for executing http requests
    :return: created customer user model
    """
    customer_user = TestDataGenerator.generate_basic_user()
    customer_user.role_id = config.role_name_id_map["customer"]
    create_customer_user_response = await users_api.create(customer_user)

    assert create_customer_user_response.ok, "Failed to create session customer user.\n" \
                                             f"Request status code: {create_customer_user_response.status}\n" \
                                             f"Response message: {await create_customer_user_response.text()}"

    create_customer_user_response_json = await create_customer_user_response.json()
    customer_user.id = create_customer_user_response_json["id"]

    yield customer_user

    http_task_group.create_task(users_api.delete(customer_user.id, auth=UserApi.get_auth(customer_user)))


@pytest.fixture(scope="session")
async def session_manager_user(config: Config, users_api: UserApi, http_task_group: TaskGroup) -> User:
    """Generate, create and return manager user in session scope

    :param config: current test environment config
    :param users_api: initialized User API
    :param http_task_group: async task group for executing http requests
    :return: created manager user model
    """
    manager_user = TestDataGenerator.generate_basic_user()
    manager_user.role_id = config.role_name_id_map["manager"]
    create_manager_user_response = await users_api.create(manager_user)

    assert create_manager_user_response.ok, "Failed to create session manager user.\n" \
                                            f"Request status code: {create_manager_user_response.status}\n" \
                                            f"Response message: {await create_manager_user_response.text()}"

    create_user_response_json = await create_manager_user_response.json()
    manager_user.id = create_user_response_json["id"]

    yield manager_user

    http_task_group.create_task(users_api.delete(manager_user.id, auth=UserApi.get_auth(manager_user)))


@pytest.fixture
async def customer_user(config: Config, users_api: UserApi, generated_user: User, http_task_group: TaskGroup) -> User:
    """Generate, create and return customer user in functional scope

    :param config: current test environment config
    :param users_api: initialized User API
    :param generated_user: generated user model
    :param http_task_group: async task group for executing http requests
    :return: created customer user model
    """
    generated_user.role_id = config.role_name_id_map["customer"]

    create_user_response = await users_api.create(generated_user)
    create_user_response_json = await create_user_response.json()
    generated_user.id = create_user_response_json["id"]

    yield generated_user

    if create_user_response.ok:
        http_task_group.create_task(users_api.delete(generated_user.id, auth=UserApi.get_auth(generated_user)))


@pytest.fixture
async def created_user_response(users_api: UserApi, generated_user: User, http_task_group: TaskGroup) -> ClientResponse:
    """Generate user, create it and return create user response

    :param users_api: initialized User API
    :param generated_user: generated user model
    :param http_task_group: async task group for executing http requests
    :return: create generated user response
    """
    create_user_response = await users_api.create(generated_user)

    yield create_user_response

    if create_user_response.ok:
        try:
            create_user_response_json = await create_user_response.json()
            user_id_to_delete = create_user_response_json["id"]
            http_task_group.create_task(users_api.delete(user_id_to_delete, auth=UserApi.get_auth(generated_user)))
        except (ContentTypeError, JSONDecodeError, KeyError, ValueError) as error:
            logging.error("Can not delete created user, error: %s", error)


@pytest.fixture
async def updated_user_response(test_data: dict, customer_user: User, users_api: UserApi) -> ClientResponse:
    """Update created customer user in the function scope and return response

    :param test_data: dict with the current test data
    :param customer_user: generated and created customer user
    :param users_api: initialized User API
    :return: update customer user response
    """
    attributes_to_set = test_data.get("new_user_attributes", {})

    update_user_response = await users_api.update(
        customer_user.id, attributes_to_set, auth=UserApi.get_auth(customer_user))

    if update_user_response.ok:
        old_attributes = asdict(customer_user)
        old_attributes.update(attributes_to_set)
        customer_user.update(old_attributes)

    return update_user_response


@pytest.fixture
async def deleted_user_response(users_api: UserApi, generated_user: User) -> ClientResponse:
    """Generate user, create it, delete it and return response to delete id

    :param users_api: initialized User API
    :param generated_user: generated user model
    :return: delete generated user response
    """
    create_user_response = await users_api.create(generated_user)

    assert create_user_response.ok, "Failed to create user for deletion test.\n" \
                                    f"Request status code: {create_user_response.status}\n" \
                                    f"Response message: {await create_user_response.text()}"

    create_user_response_json = await create_user_response.json()
    created_user_id = create_user_response_json["id"]
    delete_user_response = await users_api.delete(created_user_id, auth=UserApi.get_auth(generated_user))
    return delete_user_response


@pytest.fixture
async def get_session_customer_user_response(session_customer_user: User, users_api: UserApi) -> ClientResponse:
    """Send request to get session customer user and return response

    :param session_customer_user: generated and created customer user model
    :param users_api: initialized User API
    :return: get session customer user response
    """
    return await users_api.get(session_customer_user.id, auth=UserApi.get_auth(session_customer_user))


@pytest.fixture
async def get_customer_user_response(customer_user: User, users_api: UserApi) -> ClientResponse:
    """Send request to get session customer user and return response

    :param customer_user: generated and created customer user model
    :param users_api: initialized User API
    :return: get customer user response
    """
    return await users_api.get(customer_user.id, auth=UserApi.get_auth(customer_user))


@pytest.fixture
async def get_all_users_response(session_customer_user: User, users_api: UserApi) -> ClientResponse:
    """Send request to get all users and return response

    :param session_customer_user: existing users for creds to use
    :param users_api: initialized User API
    :return: get all users response
    """
    return await users_api.get_all(auth=UserApi.get_auth(session_customer_user))
