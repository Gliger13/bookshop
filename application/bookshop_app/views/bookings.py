"""Bookings views

Module contains routes for bookings blueprint that includes product booking,
booking management, booking overview functionality
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from bookshop_app.data_access_objects.booking import BookingDAO
from bookshop_app.models.role import UserRole

__all__ = ["bookings_blueprint"]

bookings_blueprint = Blueprint(
    name="bookings_blueprint", import_name=__name__, static_folder="static", template_folder="templates"
)


@bookings_blueprint.route("/bookings", methods=["GET"])
@login_required
def bookings_page() -> str:
    """Route for the GET request to the bookings endpoint"""
    bookings = BookingDAO.get_all()
    if current_user.role.name not in [UserRole.MANAGER, UserRole.ADMIN]:
        bookings = [booking for booking in bookings if booking.user_id == current_user.id]
    return render_template("bookings/bookings.html", user=current_user, bookings=bookings)
