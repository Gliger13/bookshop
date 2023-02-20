"""Fake booking data access object"""
from typing import Optional

from bookshop_app.models.booking import BookingModel
from bookshop_app.schemas.booking import BookingSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

booking_schema = BookingSchema()


class FakeBookingDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[BookingModel] = []

    @classmethod
    def create(cls, booking: BookingModel) -> None:
        """Create booking"""
        cls._data.append(booking)

    @classmethod
    def get_by_id(cls, booking_id: int) -> Optional[BookingModel]:
        """Get booking by id"""
        for booking in cls._data:
            if booking.id == booking_id:
                return booking
        return None

    @classmethod
    def get_all(cls) -> list[BookingModel]:
        """Return all bookings"""
        return cls._data

    @classmethod
    def delete(cls, booking_id: int) -> None:
        """Delete booking"""
        cls._data = [booking for booking in cls._data if booking.id != booking_id]

    @classmethod
    def update(cls, updated_booking_model: BookingModel) -> None:
        """Update booking"""
        for booking in cls._data:
            if booking.id == updated_booking_model.id:
                cls.delete(booking.id)
                cls.create(updated_booking_model)
                break
