"""Products views

Module contains routes for the products blueprint, which includes the
functionality of creating, reading, updating, and deleting a product.
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from bookshop_app.controllers.product import ProductController
from bookshop_app.views.main import main_blueprint

__all__ = ["products_blueprint"]

products_blueprint = Blueprint(
    name="products_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@main_blueprint.route('/')
@products_blueprint.route("/products", methods=["GET"])
def products_page() -> str:
    """Route for the GET request to the products endpoint"""
    products, status_code = ProductController.get_all()
    return render_template("products/products.html", products=products, user=current_user)


@products_blueprint.route("/product/<product_id>", methods=["GET"])
def product_page(product_id: str) -> str:
    """Route for the GET request to the product endpoint"""
    return render_template("products/product.html", user=current_user)


@products_blueprint.route("/product/<product_id>", methods=["POST"])
@login_required
def product_post(product_id: str) -> str:
    """Route for the POST request to the product endpoint"""
    raise NotImplementedError()


@products_blueprint.route("/product/<product_id>", methods=["PUT"])
@login_required
def product_update(product_id: str) -> str:
    """Route for the PUT request to the product endpoint"""
    raise NotImplementedError()


@products_blueprint.route("/product/<product_id>", methods=["DELETE"])
@login_required
def product_delete(product_id: str) -> str:
    """Route for the DELETE request to the product endpoint"""
    raise NotImplementedError()
