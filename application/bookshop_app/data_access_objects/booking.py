"""Booking Data Access Object"""

from bookshop_app.database.database import db
from bookshop_app.models.booking import BookingModel


class BookingMessages:
    """Booking messages and templates"""

    BOOKING_NOT_FOUND = "Booking not found for id: {booking_id}"


class BookingDAO:
    """Data Access Object class for Booking Model"""

    @staticmethod
    def create(booking: BookingModel) -> None:
        """Create booking in database"""
        db.session.add(booking)
        db.session.commit()

    @staticmethod
    def get_all() -> list[BookingModel]:
        """Return all bookings from database"""
        return db.session.query(BookingModel).all()

    @staticmethod
    def get_by_id(booking_id: int) -> BookingModel:
        """Get booking by id from database"""
        return db.session.query(BookingModel).get_or_404(
            booking_id,
            description=BookingMessages.BOOKING_NOT_FOUND.format(booking_id=booking_id))

    @staticmethod
    def update(updated_booking: BookingModel) -> None:
        """Update booking in database"""
        db.session.merge(updated_booking)
        db.session.commit()

    @staticmethod
    def delete(booking_id: int) -> None:
        """Delete booking from database"""
        item = db.session.query(BookingModel).filter_by(id=booking_id).first()
        db.session.delete(item)
        db.session.commit()
