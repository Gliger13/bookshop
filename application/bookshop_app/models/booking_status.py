"""ORM Booking status model"""
from collections import defaultdict
from enum import Enum
from typing import Mapping

from bookshop_app.database.database import db


class BookingStatus(Enum):
    """Booking statuses"""

    SUBMITTED = 1, "submitted", "submit"
    REJECTED = 2, "rejected", "reject"
    APPROVED = 3, "approved", "approve"
    CANCELED = 4, "canceled", "cancel"
    IN_DELIVERY = 5, "in delivery", "to delivery"
    COMPLETED = 6, "completed", "complete"

    def __init__(self, code: int, status: str, transition_action: str) -> None:
        """Initialize booking status

        :param code: unique booking status code
        :param status: booking status name
        :param transition_action: verb to transit to
        """
        self.code = code
        self.status = status
        self.transition_action = transition_action

    def __hash__(self) -> int:
        """Return booking status hash based on the current status name"""
        return hash(self.status)


class BookingStatusModel(db.Model):
    """Booking ORM moke statuses"""

    TRANSITION_MAP: Mapping[BookingStatus, list[BookingStatus]] = defaultdict(
        list,
        {
            BookingStatus.SUBMITTED: [BookingStatus.REJECTED, BookingStatus.CANCELED, BookingStatus.APPROVED],
            BookingStatus.APPROVED: [BookingStatus.REJECTED, BookingStatus.CANCELED, BookingStatus.IN_DELIVERY],
            BookingStatus.IN_DELIVERY: [BookingStatus.REJECTED, BookingStatus.CANCELED, BookingStatus.COMPLETED],
        },
    )

    __tablename__ = "booking_statuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(BookingStatus), nullable=False)

    def get_available_transitions(self) -> list[BookingStatus]:
        """Get available next statuses to transfer from the current one"""
        return self.TRANSITION_MAP[self.name]
