"""Products views

Module contains routes for the products blueprint, which includes the
functionality of creating, reading, updating, and deleting a product.
"""

from flask import Blueprint, render_template

__all__ = ["products_blueprint"]

products_blueprint = Blueprint(
    name="products_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@products_blueprint.route("/products", methods=["GET"])
def products_page() -> str:
    """Route for the GET request to the products endpoint"""
    return render_template("products/products.html")


@products_blueprint.route("/product/<product_id>", methods=["GET"])
def product_page(product_id: str) -> str:
    """Route for the GET request to the product endpoint"""
    return render_template("products/product.html")


@products_blueprint.route("/product/<product_id>", methods=["POST"])
def product_post(product_id: str) -> str:
    """Route for the POST request to the product endpoint"""
    raise NotImplementedError()


@products_blueprint.route("/product/<product_id>", methods=["PUT"])
def product_update(product_id: str) -> str:
    """Route for the PUT request to the product endpoint"""
    raise NotImplementedError()


@products_blueprint.route("/product/<product_id>", methods=["DELETE"])
def product_delete(product_id: str) -> str:
    """Route for the DELETE request to the product endpoint"""
    raise NotImplementedError()
