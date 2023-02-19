"""Async Booking API

Module contains async Booking API client for sending requests to interact with
Booking API.
"""
from dataclasses import asdict
from typing import Any

from aiohttp import ClientResponse

from bookshop_test_framework.models.booking import Booking
from bookshop_test_framework.tools.api._base import BaseApi


class BookingApi(BaseApi):
    """Booking API client for sending requests to Booking API"""

    __slots__ = ()

    async def get(self, booking_id: int, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get booking with the given ID

        :param booking_id: ID of the booking to get
        :param request_kwargs: additional request arguments
        :return: response of the request to get booking with given ID
        """
        endpoint = f"/api/booking/{booking_id}"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def get_all(self, **request_kwargs: Any) -> ClientResponse:
        """Seng GET request to get all bookings

        :param request_kwargs: additional request arguments
        :return: response of the request to get all bookings
        """
        endpoint = "/api/booking"
        response = await self._session.get(endpoint, **request_kwargs)
        return response

    async def create(self, booking: Booking, **request_kwargs: Any) -> ClientResponse:
        """Seng POST request to create given booking

        :param booking: booking model to create
        :param request_kwargs: additional request arguments
        :return: response of the request to create booking
        """
        endpoint = "/api/booking"
        request_json = {name: attribute for name, attribute in asdict(booking).items() if attribute is not None}
        response = await self._session.post(endpoint, json=request_json, **request_kwargs)
        return response

    async def update(self, booking_id: int, booking_attributes: dict, **request_kwargs: Any) -> ClientResponse:
        """Seng PUT request to update booking with given ID

        :param booking_id: ID of the booking to update
        :param booking_attributes: booking attributes to update
        :param request_kwargs: additional request arguments
        :return: response of the request to update booking
        """
        endpoint = f"/api/booking/{booking_id}"
        response = await self._session.put(endpoint, json=booking_attributes, **request_kwargs)
        return response

    async def delete(self, booking_id, **request_kwargs: Any) -> ClientResponse:
        """Seng DELETE request to delete booking with given ID

        :param booking_id: ID of the booking to delete
        :param request_kwargs: additional request arguments
        :return: response of the request to delete product
        """
        endpoint = f"/api/booking/{booking_id}"
        response = await self._session.delete(endpoint, **request_kwargs)
        return response
