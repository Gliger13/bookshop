"""Booking managing fixtures

Module contains fixtures for creating, deleting, getting booking in different
testing scopes.
"""
from asyncio import TaskGroup
from typing import Optional

import pytest
from aiohttp import ClientResponse

from bookshop_test_framework.config.config import Config
from bookshop_test_framework.models.booking import Booking
from bookshop_test_framework.models.product import Product
from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api import BookingApi, UserApi


@pytest.fixture(scope="session")
async def session_booking(
    bookings_api: BookingApi,
    users_api: UserApi,
    session_product: Product,
    session_customer_user: User,
    session_manager_user: User,
    http_task_group: TaskGroup,
) -> Booking:
    """Generate, create and return booking for customer user in session scope

    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param session_product: generated and created product
    :param session_customer_user: customer user for authentication and booking
    :param session_manager_user: manager user for booking deletion authentication
    :param http_task_group: async task group for executing http requests
    :return: created booking
    """
    booking = Booking(
        product_id=session_product.id,
        user_id=session_customer_user.id,
        quantity=1,
        delivery_address=session_customer_user.address,
    )
    customer_authentication_headers = await users_api.get_auth_header(session_customer_user)
    create_booking_response = await bookings_api.create(booking, headers=customer_authentication_headers)
    assert create_booking_response.ok, (
        "Failed to create session booking.\n"
        f"Request status code: {create_booking_response.status}\n"
        f"Response message: {await create_booking_response.text()}"
    )

    create_booking_response_json = await create_booking_response.json()
    booking.id = create_booking_response_json["id"]

    yield booking

    manager_authentication_headers = await users_api.get_auth_header(session_manager_user)
    http_task_group.create_task(bookings_api.delete(booking.id, headers=manager_authentication_headers))


@pytest.fixture(scope="session")
async def session_get_booking_response(
    bookings_api: BookingApi, users_api: UserApi, session_customer_user: User, session_booking: Booking
) -> ClientResponse:
    """Get session booking with the session customer user and return response

    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param session_customer_user: customer user to use for authentication
    :param session_booking: created booking in the session scope
    :return: get booking response
    """
    authentication_headers = await users_api.get_auth_header(session_customer_user)
    return await bookings_api.get(session_booking.id, headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_get_all_bookings_response(
    bookings_api: BookingApi, users_api: UserApi, session_manager_user: User
) -> ClientResponse:
    """Send request to get all bookings and return response

    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :return: get all bookings response
    """
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await bookings_api.get_all(headers=authentication_headers)


@pytest.fixture(scope="session")
async def session_update_booking_response(
    config: Config, bookings_api: BookingApi, users_api: UserApi, session_manager_user: User, session_booking: Booking
) -> ClientResponse:
    """Send request to update given booking and return response

    :param config: current environment config for tests
    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param session_manager_user: manager user to use for authentication
    :param session_booking: updated booking model in the session scope
    :return: update booking response
    """
    attributes_to_update = {"status_id": config.status_name_id_map["rejected"]}
    authentication_headers = await users_api.get_auth_header(session_manager_user)
    return await bookings_api.update(session_booking.id, attributes_to_update, headers=authentication_headers)


@pytest.fixture
async def created_booking_response(
    bookings_api: BookingApi,
    users_api: UserApi,
    generated_booking: Booking,
    generated_user: User,
    session_manager_user: User,
    http_task_group: TaskGroup,
) -> ClientResponse:
    """Create generated booking and return response

    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param generated_booking: generated booking model
    :param generated_user: generated and created user to use for booking
    :param session_manager_user: manager user model
    :param http_task_group: async task group for executing http requests
    :return: create booking response
    """
    generated_user_auth_headers = await users_api.get_auth_header(generated_user)
    create_booking_response = await bookings_api.create(generated_booking, headers=generated_user_auth_headers)

    yield create_booking_response

    if create_booking_response.ok:
        create_booking_response_json = await create_booking_response.json()
        created_booking_id = create_booking_response_json["id"]
        manager_authentication_headers = await users_api.get_auth_header(session_manager_user)
        http_task_group.create_task(bookings_api.delete(created_booking_id, headers=manager_authentication_headers))


@pytest.fixture
async def created_booking(created_booking_response: ClientResponse, generated_booking: Booking) -> Optional[Booking]:
    """Create generated booking and return generated booking model

    :param created_booking_response: response to create generated booking
    :param generated_booking: generated booking
    :return: generated and created booking model
    """
    if created_booking_response.ok:
        created_booking_response_json = await created_booking_response.json()
        generated_booking.id = created_booking_response_json["id"]
        return generated_booking
    return None


@pytest.fixture
async def deleted_booking_response(
    bookings_api: BookingApi, users_api: UserApi, generated_booking: Booking, session_admin_user: User
) -> ClientResponse:
    """Delete generated and created booking and return response

    :param bookings_api: initialized Booking API
    :param users_api: initialized User API
    :param generated_booking: generated booking
    :param session_admin_user: admin user model
    :return: delete created booking response
    """
    authentication_headers = await users_api.get_auth_header(session_admin_user)
    create_booking_response = await bookings_api.create(generated_booking, headers=authentication_headers)
    assert create_booking_response.ok, (
        "Failed to create booking to delete later.\n"
        f"Request status code: {create_booking_response.status}\n"
        f"Response message: {await create_booking_response.text()}"
    )

    create_booking_response_json = await create_booking_response.json()
    created_booking_id = create_booking_response_json["id"]
    return await bookings_api.delete(created_booking_id, headers=authentication_headers)
