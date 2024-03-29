"""Booking routes

Module contains routes for booking manipulations.
"""
from flask import request
from flask import Response

from bookshop_app.controllers.booking import BookingController


def booking_control() -> tuple[Response | dict | list[dict], int]:
    """URL to collect information about booking or create new one

    :return: tuple of response json and status code
    """
    if request.method == "POST":
        return BookingController.create()
    return BookingController.get_all()


def booking_manipulation(booking_id: int) -> tuple[Response | dict | list[dict], int]:
    """URL to get, update or delete booking information

    :param booking_id: ID of the booking to manipulate
    :return: tuple of response json and status code
    """
    if request.method == "GET":
        return BookingController.get(booking_id)
    if request.method == "PUT":
        return BookingController.update(booking_id)
    return BookingController.delete(booking_id)
