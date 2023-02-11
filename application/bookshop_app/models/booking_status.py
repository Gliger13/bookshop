"""ORM Booking status model"""
from enum import Enum

from bookshop_app.database.database import db


class BookingStatus(Enum):
    """Booking statuses"""

    SUBMITTED = "submitted"
    REJECTED = "rejected"
    APPROVED = "approved"
    CANCELED = "canceled"
    IN_DELIVERY = "in delivery"
    COMPLETED = "completed"


class BookingStatusModel(db.Model):
    """Booking ORM moke statuses"""

    __tablename__ = "booking_statuses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(BookingStatus), nullable=False)
