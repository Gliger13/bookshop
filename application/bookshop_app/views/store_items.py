"""Store items views

Module contains routes for the store items blueprint, which includes the
functionality of creating, reading, updating, and deleting a store item.
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from bookshop_app.forms.store_item import CreateStoreItemForm, DeleteStoreItemForm, UpdateStoreItemForm
from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import required_roles
from bookshop_app.services.store_item import StoreItemService

__all__ = ["store_items_blueprint"]

store_items_blueprint = Blueprint(
    name="store_items_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@store_items_blueprint.route("/store-items", methods=["GET"])
@login_required
@required_roles([UserRole.MANAGER, UserRole.ADMIN])
def store_items_page() -> str:
    """Route for the GET request to the  store_items endpoint"""
    create_store_item_form = CreateStoreItemForm()
    update_store_item_form = UpdateStoreItemForm()
    delete_store_item_form = DeleteStoreItemForm()
    store_items, status_code = StoreItemService.get_all()
    return render_template(
        template_name_or_list="store_items/store_items.html",
        user=current_user,
        store_items=store_items,
        create_store_item_form=create_store_item_form,
        update_store_item_form=update_store_item_form,
        delete_store_item_form=delete_store_item_form,
    )
