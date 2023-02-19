"""Async User API

Module contains async User API client for sending requests to interact with
User API.
"""
from dataclasses import asdict
from typing import Any

from aiohttp import BasicAuth, ClientResponse

from bookshop_test_framework.models.user import User
from bookshop_test_framework.tools.api._base import BaseApi


class UserApi(BaseApi):
    """User API client for sending requests to User API"""

    __slots__ = ()

    @classmethod
    def get_auth(cls, user: User) -> BasicAuth:
        """Get authentication for the given user

        :param user: user to use in authentication
        :return: authentication for the given user
        """
        return BasicAuth(login=user.login, password=user.password)

    async def get(self, user_id: int, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get user with given ID

        :param user_id: ID of the user to get
        :param request_kwargs: additional request arguments
        :return: response of the request to get user with given ID
        """
        endpoint = f"/api/user/{user_id}"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def get_all(self, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get all users

        :param request_kwargs: additional request arguments
        :return: response of the request to get all users
        """
        endpoint = "/api/user"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def create(self, user: User, **request_kwargs: Any) -> ClientResponse:
        """Seng POST request to create given user

        :param user: user model to create
        :param request_kwargs: additional request arguments
        :return: response of the request to create user
        """
        endpoint = "/api/user"
        request_json = {name: attribute for name, attribute in asdict(user).items() if attribute is not None}
        response = await self._session.post(endpoint, json=request_json, **request_kwargs)
        return response

    async def update(self, user_id: int, user_attributes: dict, **request_kwargs: Any) -> ClientResponse:
        """Seng PUT request to update user with given ID and with given attrs

        :param user_id: ID of the user to update
        :param user_attributes: user attributes to update
        :param request_kwargs: additional request arguments
        :return: response of the request to update user
        """
        endpoint = f"/api/user/{user_id}"
        response = await self._session.put(endpoint, json=user_attributes, **request_kwargs)
        return response

    async def delete(self, user_id, **request_kwargs: Any) -> ClientResponse:
        """Seng DELETE request to delete user with given ID

        :param user_id: ID of the user to delete
        :param request_kwargs: additional request arguments
        :return: response of the request to delete user
        """
        endpoint = f"/api/user/{user_id}"
        response = await self._session.delete(endpoint, **request_kwargs)
        return response
