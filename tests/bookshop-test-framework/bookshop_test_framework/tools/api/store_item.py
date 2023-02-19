"""Async Store Item API

Module contains async Store Item API client for sending requests to interact
with Store Item API.
"""
from dataclasses import asdict
from typing import Any

from aiohttp import ClientResponse

from bookshop_test_framework.models.store_item import StoreItem
from bookshop_test_framework.tools.api._base import BaseApi


class StoreItemApi(BaseApi):
    """Store Item API client for sending requests to Store Item API"""

    __slots__ = ()

    async def get(self, store_item_id: int, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get store item with the given ID

        :param store_item_id: ID of the store item to get
        :param request_kwargs: additional request arguments
        :return: response of the request to get store item with given ID
        """
        endpoint = f"/api/store-item/{store_item_id}"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def get_all(self, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get all store items

        :param request_kwargs: additional request arguments
        :return: response of the request to get all store items
        """
        endpoint = "/api/store-item"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def create(self, store_item: StoreItem, **request_kwargs: Any) -> ClientResponse:
        """Seng POST request to create given store item

        :param store_item: store item model to create
        :param request_kwargs: additional request arguments
        :return: response of the request to create store item
        """
        endpoint = "/api/store-item"
        request_json = {name: attribute for name, attribute in asdict(store_item).items() if attribute is not None}
        response = await self._session.post(endpoint, json=request_json, **request_kwargs)
        return response

    async def update(self, store_item_id: int, store_item_attributes: dict, **request_kwargs: Any) -> ClientResponse:
        """Seng PUT request to update store item with given ID

        :param store_item_id: ID of the store item to update
        :param store_item_attributes: store item attributes to update
        :param request_kwargs: additional request arguments
        :return: response of the request to update store item
        """
        endpoint = f"/api/store-item/{store_item_id}"
        response = await self._session.put(endpoint, json=store_item_attributes, **request_kwargs)
        return response

    async def delete(self, store_item_id, **request_kwargs: Any) -> ClientResponse:
        """Seng DELETE request to delete store item with given ID

        :param store_item_id: ID of the store item to delete
        :param request_kwargs: additional request arguments
        :return: response of the request to delete store item
        """
        endpoint = f"/api/store-item/{store_item_id}"
        response = await self._session.delete(endpoint, **request_kwargs)
        return response
