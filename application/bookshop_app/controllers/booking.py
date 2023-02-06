"""Booking controller"""
from flask import Response
from bookshop_app.authenticator import auth
from bookshop_app.services.booking import BookingService


class BookingController:
    """Controller for Booking"""

    @staticmethod
    def get(booking_id: int) -> dict:
        """Get booking resource by booking id"""
        return BookingService.get(booking_id)

    @staticmethod
    @auth.login_required
    def create() -> Response | tuple[dict, int]:
        """Create booking resource"""
        return BookingService.create()

    @staticmethod
    @auth.login_required
    def delete(booking_id: int) -> tuple[dict[str, str], int]:
        """Delete booking resource"""
        return BookingService.delete(booking_id)

    @staticmethod
    @auth.login_required
    def update(booking_id: int) -> Response | tuple[dict, int]:
        """Update booking resource"""
        return BookingService.update(booking_id)
