"""Product routes

Module contains routes for user manipulations.
"""

from flask import request

from bookshop_app.controllers.product import ProductController


def product_control():
    """URL to collect information about users or create new one."""
    if request.method == 'POST':
        return ProductController.create()
    else:
        return ProductController.get_all()


def product_manipulation(product_id: int):
    """URL to get, update or delete user information."""
    if request.method == 'GET':
        return ProductController.get(product_id)
    elif request.method == 'PUT':
        return ProductController.update(product_id)
    else:
        return ProductController.delete(product_id)
