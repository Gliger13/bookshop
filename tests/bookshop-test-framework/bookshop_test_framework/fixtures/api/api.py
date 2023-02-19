"""HTTP session and api fixtures

Module contains fixtures for creating and managing client session for http
requests. Provides fixtures with initialized bookshop APIs.
"""
from asyncio import ProactorEventLoop, TaskGroup

import pytest
from aiohttp import ClientSession, TCPConnector
from pytest_asyncio import fixture

from bookshop_test_framework.config.config import Config
from bookshop_test_framework.tools.api import BookingApi, ProductApi, StoreItemApi, UserApi


@fixture(scope="session")
async def http_session(config: Config, event_loop: ProactorEventLoop, http_task_group: TaskGroup) -> ClientSession:
    """Client session for http requests

    Create and return client session for http requests using API URL from the
    config and general tests event loop. After test session ends, wait for all
    http requests from the http task group to complete and close the client
    session.

    :param config: test config for the current environment
    :param event_loop: async event loop in the session scope
    :param http_task_group: async task group for all http request related tasks
    :return: initialized client session
    """
    connector = TCPConnector(limit=500)
    async with ClientSession(config.api_url, trust_env=True, loop=event_loop, connector=connector) as session:
        async with http_task_group:
            yield session


@pytest.fixture(scope="session")
def users_api(http_session: ClientSession) -> UserApi:
    """Initialize and return User API

    :param http_session: initialized client session
    :return: initialized User API
    """
    return UserApi(http_session)


@pytest.fixture(scope="session")
def products_api(http_session: ClientSession) -> ProductApi:
    """Initialize and return Product API

    :param http_session: initialized client session
    :return: initialized Product API
    """
    return ProductApi(http_session)


@pytest.fixture(scope="session")
def bookings_api(http_session: ClientSession) -> BookingApi:
    """Initialize and return Booking API

    :param http_session: initialized client session
    :return: initialized Booking API
    """
    return BookingApi(http_session)


@pytest.fixture(scope="session")
def store_items_api(http_session: ClientSession) -> StoreItemApi:
    """Initialize and return Store Item API

    :param http_session: initialized client session
    :return: initialized Store Item API
    """
    return StoreItemApi(http_session)
