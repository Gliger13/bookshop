"""Store items views

Module contains routes for the store items blueprint, which includes the
functionality of creating, reading, updating, and deleting a store item.
"""

from flask import Blueprint, render_template

__all__ = ["store_items_blueprint"]

store_items_blueprint = Blueprint(
    name="store_items_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@store_items_blueprint.route("/store-items", methods=["GET"])
def store_items_page() -> str:
    """Route for the GET request to the  store_items endpoint"""
    return render_template("store_items/store_items.html")


@store_items_blueprint.route("/store-items/<store_item_id>", methods=["GET"])
def store_item_page(store_item_id: str) -> str:
    """Route for the GET request to the store item endpoint"""
    return render_template("store_items/store_item.html")


@store_items_blueprint.route("/store-items/<store_item_id>", methods=["POST"])
def  store_item_post(store_item_id: str) -> str:
    """Route for the POST request to the store item endpoint"""
    raise NotImplementedError()


@store_items_blueprint.route("/store-items/<store_item_id>", methods=["PUT"])
def  store_item_update(store_item_id: str) -> str:
    """Route for the PUT request to the store item endpoint"""
    raise NotImplementedError()


@store_items_blueprint.route("/store-items/<store_item_id>", methods=["DELETE"])
def  store_item_delete(store_item_id: str) -> str:
    """Route for the DELETE request to the store item endpoint"""
    raise NotImplementedError()
