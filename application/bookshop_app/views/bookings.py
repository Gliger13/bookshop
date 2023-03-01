"""Bookings views

Module contains routes for bookings blueprint that includes product booking,
booking management, booking overview functionality
"""
from flask import Blueprint, render_template
from flask_login import current_user, login_required

from bookshop_app.controllers.booking import BookingController

__all__ = ["bookings_blueprint"]

bookings_blueprint = Blueprint(
    name="bookings_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@bookings_blueprint.route("/bookings", methods=["GET"])
@login_required
def bookings_page() -> str:
    """Route for the GET request to the bookings endpoint"""
    bookings, status_code = BookingController.get_all()
    return render_template("bookings/bookings.html", user=current_user, bookings=bookings)


@bookings_blueprint.route("/booking/<booking_id>", methods=["GET"])
@login_required
def booking_page(booking_id: str) -> str:
    """Route for the GET request to the booking endpoint"""
    return render_template("bookings/booking.html", user=current_user)


@bookings_blueprint.route("/booking/<booking_id>", methods=["POST"])
def booking_post(booking_id: str) -> str:
    """Route for the POST request to the booking endpoint"""
    raise NotImplementedError()


@bookings_blueprint.route("/booking/<booking_id>", methods=["PUT"])
def booking_update(booking_id: str) -> str:
    """Route for the PUT request to the booking endpoint"""
    raise NotImplementedError()


@bookings_blueprint.route("/booking/<booking_id>", methods=["DELETE"])
def booking_delete(booking_id: str) -> str:
    """Route for the DELETE request to the booking endpoint"""
    raise NotImplementedError()
