"""Booking service

Module contains Booking Service that provides methods with CRUD operations for
booking resource.
"""

from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.booking import BookingDAO
from bookshop_app.schemas.booking import BookingSchema

booking_schema = BookingSchema()


class BookingService:
    """Booking Service

    Provides service methods that support CRUD operations for booking resource
    """

    @staticmethod
    def get(booking_id: int) -> dict:
        """Get booking resource by id"""
        booking_data = BookingDAO.get_by_id(booking_id)
        return booking_schema.dump(booking_data)

    @staticmethod
    def create() -> Response | tuple[dict, int]:
        """Create booking resource"""
        create_booking_json = request.get_json()
        booking_data = booking_schema.load(create_booking_json)
        BookingDAO.create(booking_data)
        return booking_schema.dump(booking_data), codes.created

    @staticmethod
    def delete(booking_id: int) -> tuple[dict[str, str], int]:
        """Delete booking resource"""
        BookingDAO.get_by_id(booking_id)
        BookingDAO.delete(booking_id)
        return {'message': 'Booking deleted successfully'}, codes.ok

    @staticmethod
    def update(booking_id: int) -> Response | tuple[dict, int]:
        """Update booking resource"""
        try:
            booking_model = BookingDAO.get_by_id(booking_id)
            old_booking_data = booking_schema.dump(booking_model)
            update_booking_request_json = request.get_json()
            old_booking_data.update(update_booking_request_json)
            updated_booking_data = booking_schema.load(old_booking_data)
            BookingDAO.update(updated_booking_data)
            return booking_schema.dump(updated_booking_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request, title="Bad Request", type="about:blank")
