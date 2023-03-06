"""Database events

Module contains database event handlers. Responsible for preparing and adding
initial data after specific table is created.
"""

import logging
from typing import Any

from sqlalchemy import Table
from sqlalchemy.engine import Connection
from sqlalchemy.event import listens_for

from bookshop_app.models.booking_status import BookingStatus, BookingStatusModel
from bookshop_app.models.role import RoleModel, UserRole

__all__ = ["create_roles_after_table_creation", "create_booking_statuses_after_table_creation"]


@listens_for(RoleModel.__table__, "after_create")
def create_roles_after_table_creation(target: Table, connection: Connection, **_: Any) -> None:
    """Create roles specified in UserRole enum after creating roles table

    :param target: target role table that has just been created
    :param connection: engine connection
    """
    logging.info("Roles table has just been created. Populating it with all defined enum roles...")
    roles_to_create = [{"id": index + 1, "name": role.name} for index, role in enumerate(UserRole)]
    connection.execute(target.insert(), *roles_to_create)
    logging.debug("Inserted roles `%s`", roles_to_create)
    logging.info("Roles table has been populated with all defined enum roles")


@listens_for(BookingStatusModel.__table__, "after_create")
def create_booking_statuses_after_table_creation(target: Table, connection: Connection, **_: Any) -> None:
    """Create roles specified in UserRole enum after creating roles table

    :param target: target bookings statuses table that has just been created
    :param connection: engine connection
    """
    logging.info("Booking statuses table has just been created. Populating it with all defined enum statuses...")
    statuses_to_create = [{"id": status.code, "name": status.status} for status in BookingStatus]
    connection.execute(target.insert(), *statuses_to_create)
    logging.debug("Inserted booking statuses `%s`", statuses_to_create)
    logging.info("Booking statuses table has been populated with all defined enum statuses")
