"""Product routes

Module contains routes for user manipulations.
"""

from flask import request, Response

from bookshop_app.controllers.product import ProductController


def product_control() -> tuple[Response | dict | list[dict], int]:
    """URL to collect information about products or create new one

    :return: tuple of response json and status code
    """
    if request.method == 'POST':
        return ProductController.create()
    else:
        return ProductController.get_all()


def product_manipulation(product_id: int) -> tuple[Response | dict | list[dict], int]:
    """URL to get, update or delete product information

    :param product_id: ID of the product to manipulate
    :return: tuple of response json and status code
    """
    if request.method == 'GET':
        return ProductController.get(product_id)
    elif request.method == 'PUT':
        return ProductController.update(product_id)
    else:
        return ProductController.delete(product_id)
