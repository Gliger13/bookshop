"""Async Product API

Module contains async Product API client for sending requests to interact with
Product API.
"""
from dataclasses import asdict
from typing import Any

from aiohttp import ClientResponse

from bookshop_test_framework.models.product import Product
from bookshop_test_framework.tools.api._base import BaseApi


class ProductApi(BaseApi):
    """Product API client for sending requests to Product API"""

    __slots__ = ()

    async def get(self, product_id: int, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get product with given ID

        :param product_id: ID of the product to get
        :param request_kwargs: additional request arguments
        :return: response of the request to get product with given ID
        """
        endpoint = f"/api/product/{product_id}"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def get_all(self, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get all products

        :param request_kwargs: additional request arguments
        :return: response of the request to get all products
        """
        endpoint = "/api/product"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def create(self, product: Product, **request_kwargs: Any) -> ClientResponse:
        """Seng POST request to create given product

        :param product: product model to create
        :param request_kwargs: additional request arguments
        :return: response of the request to create product
        """
        endpoint = "/api/product"
        request_json = {name: attribute for name, attribute in asdict(product).items() if attribute is not None}
        response = await self._session.post(endpoint, json=request_json, **request_kwargs)
        return response

    async def update(self, product_id: int, product_attributes: dict, **request_kwargs: Any) -> ClientResponse:
        """Seng PUT request to update product with given ID

        :param product_id: ID of the product to update
        :param product_attributes: product attributes to update
        :param request_kwargs: additional request arguments
        :return: response of the request to update product
        """
        endpoint = f"/api/product/{product_id}"
        response = await self._session.put(endpoint, json=product_attributes, **request_kwargs)
        return response

    async def delete(self, product_id, **request_kwargs: Any) -> ClientResponse:
        """Seng DELETE request to delete product with given ID

        :param product_id: ID of the product to delete
        :param request_kwargs: additional request arguments
        :return: response of the request to delete product
        """
        endpoint = f"/api/product/{product_id}"
        response = await self._session.delete(endpoint, **request_kwargs)
        return response
