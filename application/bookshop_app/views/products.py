"""Products views

Module contains routes for the products blueprint, which includes the
functionality of creating, reading, updating, and deleting a product.
"""
from flask import Blueprint, render_template
from flask_login import current_user

from bookshop_app.controllers.product import ProductController
from bookshop_app.forms.product import CreateProductForm, DeleteProductForm, UpdateProductForm
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
    create_product_form = CreateProductForm()
    update_product_form = UpdateProductForm()
    delete_product_form = DeleteProductForm()
    return render_template(
        template_name_or_list="products/products.html",
        products=products,
        user=current_user,
        create_product_form=create_product_form,
        update_product_form=update_product_form,
        delete_product_form=delete_product_form
    )


@products_blueprint.route("/product/<product_id>", methods=["GET"])
def product_page(product_id: str) -> str:
    """Route for the GET request to the product endpoint"""
    return render_template("products/product.html", user=current_user)
