"""Store item routes

Module contains routes for store item manipulations.
"""

from flask import request, Response

from bookshop_app.controllers.store_item import StoreItemController


def store_item_control() -> tuple[Response | dict | list[dict], int]:
    """URL to collect information about store items or create new one

    :return: tuple of response json and status code
    """
    if request.method == "POST":
        return StoreItemController.create()
    return StoreItemController.get_all()


def store_item_manipulation(store_item_id: int) -> tuple[Response | dict | list[dict], int]:
    """URL to get, update or delete store item information

    :param store_item_id: ID of the store item to manipulate
    :return: tuple of response json and status code
    """
    if request.method == "GET":
        return StoreItemController.get(store_item_id)
    if request.method == "PUT":
        return StoreItemController.update(store_item_id)
    return StoreItemController.delete(store_item_id)
