"""Fake booking status data access object"""
from typing import Optional

from bookshop_app.models.booking_status import BookingStatus
from bookshop_app.models.booking_status import BookingStatusModel
from bookshop_app.schemas.booking_status import BookingStatusSchema
from bookshop_test_framework.mocks.dao.base import BaseFakeDAO

booking_status_schema = BookingStatusSchema()


class FakeBookingStatusDAO(BaseFakeDAO):
    """Data Access Object that uses class attribute for storing data"""

    _data: list[BookingStatusModel] = [
        *[BookingStatusModel(id=index + 1, name=status) for index, status in enumerate(BookingStatus)]
    ]

    @classmethod
    def get_by_id(cls, booking_status_id: int) -> Optional[BookingStatusModel]:
        """Get booking status by id"""
        for booking_status in cls._data:
            if booking_status.id == booking_status_id:
                return booking_status
        return None

    @classmethod
    def get_all(cls) -> list[BookingStatusModel]:
        """Return all booking statuses"""
        return cls._data
