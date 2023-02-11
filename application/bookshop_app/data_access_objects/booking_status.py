"""Booking Status Data Access Object"""
from bookshop_app import BookingStatusModel
from bookshop_app.database import db


class BookingStatusMessages:
    """Booking statuses messages and templates"""

    BOOKING_STATUS_NOT_FOUND = "Booking status was not found with id: {booking_status_id}"


class BookingStatusDAO:
    """Data Access Object class for Booking Status Model"""

    @staticmethod
    def get_all() -> list[BookingStatusModel]:
        """Return all booking statuses from database"""
        return db.session.query(BookingStatusModel).all()

    @staticmethod
    def get_by_id(booking_status_id: int) -> BookingStatusModel:
        """Get booking status by id from database"""
        return db.session.query(BookingStatusModel).get_or_404(
            booking_status_id,
            description=BookingStatusMessages.BOOKING_STATUS_NOT_FOUND.format(booking_status_id=booking_status_id))
