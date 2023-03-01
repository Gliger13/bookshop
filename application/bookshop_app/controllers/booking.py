"""Booking controller"""
from flask import Response

from bookshop_app.models.role import UserRole
from bookshop_app.services.authentication import filter_bookings_by_roles, multi_auth, \
    required_creating_booking_for_self_or_roles, required_own_given_booking_id_or_roles
from bookshop_app.services.booking import BookingService


class BookingController:
    """Controller for Booking"""

    @staticmethod
    @multi_auth.login_required
    @filter_bookings_by_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def get_all() -> tuple[list[dict], int]:
        """Get all booking resources"""
        return BookingService.get_all()

    @staticmethod
    @multi_auth.login_required
    @required_own_given_booking_id_or_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def get(booking_id: int) -> tuple[dict, int]:
        """Get booking resource by booking id"""
        return BookingService.get(booking_id)

    @staticmethod
    @multi_auth.login_required
    @required_creating_booking_for_self_or_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def create() -> Response | tuple[dict, int]:
        """Create booking resource"""
        return BookingService.create()

    @staticmethod
    @multi_auth.login_required(role=[UserRole.ADMIN])
    def delete(booking_id: int) -> tuple[dict[str, str], int]:
        """Delete booking resource"""
        return BookingService.delete(booking_id)

    @staticmethod
    @multi_auth.login_required
    @required_own_given_booking_id_or_roles(roles=[UserRole.MANAGER, UserRole.ADMIN])
    def update(booking_id: int) -> Response | tuple[dict, int]:
        """Update booking resource"""
        return BookingService.update(booking_id)
