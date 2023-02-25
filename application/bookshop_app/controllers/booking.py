"""Booking controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import auth
from bookshop_app.services.booking import BookingService


class BookingController:
    """Controller for Booking"""

    @staticmethod
    @auth.login_required(role=[UserRole.ADMIN.name, UserRole.MANAGER.name])
    def get_all() -> tuple[list[dict], int]:
        """Get all booking resources"""
        return BookingService.get_all()

    @staticmethod
    def get(booking_id: int) -> tuple[dict, int]:
        """Get booking resource by booking id"""
        return BookingService.get(booking_id)

    @staticmethod
    @auth.login_required
    def create() -> Response | tuple[dict, int]:
        """Create booking resource"""
        return BookingService.create()

    @staticmethod
    @auth.login_required(role=[UserRole.ADMIN.name])
    def delete(booking_id: int) -> tuple[dict[str, str], int]:
        """Delete booking resource"""
        return BookingService.delete(booking_id)

    @staticmethod
    @auth.login_required
    def update(booking_id: int) -> Response | tuple[dict, int]:
        """Update booking resource"""
        return BookingService.update(booking_id)
