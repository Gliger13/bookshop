"""Bookings views

Module contains routes for bookings blueprint that includes product booking,
booking management, booking overview functionality
"""

from flask import Blueprint, render_template

__all__ = ["bookings_blueprint"]

bookings_blueprint = Blueprint(
    name="bookings_blueprint",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)


@bookings_blueprint.route("/bookings", methods=["GET"])
def bookings_page() -> str:
    """Route for the GET request to the bookings endpoint"""
    return render_template("bookings/bookings.html")


@bookings_blueprint.route("/booking/<booking_id>", methods=["GET"])
def booking_page(booking_id: str) -> str:
    """Route for the GET request to the booking endpoint"""
    return render_template("bookings/booking.html")


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
