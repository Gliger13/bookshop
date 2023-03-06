"""Users views

Module contains routes for the users blueprint, which includes the
functionality of creating, reading, updating, and deleting all users.
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from bookshop_app.controllers.user import UserController
from bookshop_app.forms.authentication import DeleteUserByIdForm, DeleteUserForm, RegistrationForm, \
    UpdateUserByIdForm, UpdateUserForm
from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import required_roles
from bookshop_app.services.user import UserService

__all__ = ["users_blueprint"]

users_blueprint = Blueprint(
    name="users_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@users_blueprint.route("/users", methods=["GET"])
@login_required
@required_roles([UserRole.MANAGER, UserRole.ADMIN])
def users_page() -> str:
    """Route for the GET request to the users endpoint"""
    users, status_code = UserService.get_all()
    create_user_form = RegistrationForm()
    update_user_form = UpdateUserForm()
    delete_user_form = DeleteUserForm()
    return render_template(
        template_name_or_list="users/users.html",
        user=current_user,
        users=users,
        create_user_form=create_user_form,
        update_user_form=update_user_form,
        delete_user_form=delete_user_form,
    )


@users_blueprint.route("/user/<user_id>/", methods=["GET"])
@login_required
def user_page(user_id: str) -> str:
    """Route for the GET request to the user endpoint"""
    user, status_code = UserService.get(int(user_id))

    update_user_by_id_form = UpdateUserByIdForm()
    update_user_by_id_form.id.data = user["id"]
    update_user_by_id_form.login.data = user["login"]
    update_user_by_id_form.email.data = user["email"]
    update_user_by_id_form.phone.data = user["phone"]
    update_user_by_id_form.name.data = user["name"]
    update_user_by_id_form.address.data = user["address"]
    update_user_by_id_form.role_id.data = user["role_id"]

    delete_user_by_id_form = DeleteUserByIdForm()
    delete_user_by_id_form.id.data = user["id"]
    return render_template(
        template_name_or_list="users/user.html",
        user=current_user,
        target_user=user,
        update_user_by_id_form=update_user_by_id_form,
        delete_user_by_id_form=delete_user_by_id_form
    )
