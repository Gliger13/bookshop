"""Products views

Module contains routes for the products blueprint, which includes the
functionality of creating, reading, updating, and deleting a product.
"""
from flask import Blueprint, render_template
from flask_login import current_user

from bookshop_app.controllers.product import ProductController
from bookshop_app.forms.booking import BookProductForm
from bookshop_app.forms.product import (
    CreateProductForm,
    DeleteProductByIdForm,
    DeleteProductForm,
    UpdateProductByIdForm,
    UpdateProductForm,
)
from bookshop_app.views.main import main_blueprint

__all__ = ["products_blueprint"]

products_blueprint = Blueprint(
    name="products_blueprint", import_name=__name__, static_folder="static", template_folder="templates"
)


@main_blueprint.route("/")
@products_blueprint.route("/products", methods=["GET"])
def products_page() -> str:
    """Route for the GET request to the products endpoint"""
    products, _ = ProductController.get_all()
    create_product_form = CreateProductForm()
    update_product_form = UpdateProductForm()
    delete_product_form = DeleteProductForm()
    return render_template(
        template_name_or_list="products/products.html",
        products=products,
        user=current_user,
        create_product_form=create_product_form,
        update_product_form=update_product_form,
        delete_product_form=delete_product_form,
    )


@products_blueprint.route("/product/<product_id>/", methods=["GET"])
def product_page(product_id: str) -> str:
    """Route for the GET request to the product endpoint"""
    product_id = int(product_id)
    product, _ = ProductController.get(product_id)

    book_product_by_id_form = BookProductForm()
    book_product_by_id_form.product_id.data = product_id
    book_product_by_id_form.user_id.data = current_user.id
    book_product_by_id_form.delivery_address.data = current_user.address

    update_product_by_id_form = UpdateProductByIdForm()
    update_product_by_id_form.id.data = product_id
    update_product_by_id_form.name.data = product["name"]
    update_product_by_id_form.author.data = product["author"]
    update_product_by_id_form.description.data = product["description"]
    update_product_by_id_form.price.data = product["price"]

    delete_product_by_id_form = DeleteProductByIdForm()
    delete_product_by_id_form.id.data = product_id
    return render_template(
        template_name_or_list="products/product.html",
        product=product,
        user=current_user,
        book_product_by_id_form=book_product_by_id_form,
        update_product_by_id_form=update_product_by_id_form,
        delete_product_by_id_form=delete_product_by_id_form,
    )
