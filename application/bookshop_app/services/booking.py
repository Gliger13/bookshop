"""Booking service

Module contains Booking Service that provides methods with CRUD operations for
booking resource.
"""
from flask import jsonify, request, Response
from marshmallow import ValidationError
from requests import codes
from sqlalchemy.exc import IntegrityError

from bookshop_app.data_access_objects.booking import BookingDAO
from bookshop_app.data_access_objects.booking_status import BookingStatusDAO
from bookshop_app.data_access_objects.product import ProductDAO
from bookshop_app.data_access_objects.user import UserDAO
from bookshop_app.models.booking import BookingModel
from bookshop_app.models.role import UserRole
from bookshop_app.models.user import UserModel
from bookshop_app.schemas.booking import BookingSchema

booking_schema = BookingSchema()
booking_list_schema = BookingSchema(many=True)


class BookingService:
    """Booking Service

    Provides service methods that support CRUD operations for booking resource
    """

    @staticmethod
    def get_all() -> tuple[list[dict], int]:
        """Get all booking resources

        :return: list of all booking attributes
        """
        all_booking_data = BookingDAO.get_all()
        return booking_list_schema.dump(all_booking_data), codes.ok

    @staticmethod
    def get_permitted_bookings(actor_user: UserModel) -> list[BookingModel]:
        """Get bookings that can view given actor user

        TODO: Replace method by

        :param actor_user:
        :return:
        """
        permitted_bookings: list[BookingModel] = []
        for booking in BookingDAO.get_all():
            if booking.user_id == actor_user.id or actor_user.role.name.name in [UserRole.MANAGER, UserRole.ADMIN]:
                permitted_bookings.append(booking)
        return permitted_bookings

    @staticmethod
    def get(booking_id: int) -> tuple[dict, int]:
        """Get booking resource attributes with given id

        :param booking_id: id of the booking resource to delete
        :raise HTTPException: if given booking id does not exist
        :return: booking with given id
        """
        booking_data = BookingDAO.get_by_id(booking_id)
        return booking_schema.dump(booking_data), codes.ok

    @staticmethod
    def create() -> tuple[dict | Response, int]:
        """Create booking resource

        Validate and load create booking request json using booking schema.
        Check for existence of user id, booking status id, product id. Create
        booking model using Data Access Object.

        :raise HTTPException: raise if:
          - there are validation errors with create booking request json
          - given user id does not exist
          - given booking status id does not exist
          - given product id does not exist
        :return: tuple of response json and status code
        """
        try:
            create_booking_json = request.get_json()
            booking_data = booking_schema.load(create_booking_json)
            BookingService.validate_create_or_update_booking_request(create_booking_json)
            BookingDAO.create(booking_data)
            return booking_schema.dump(booking_data), codes.created
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def delete(booking_id: int) -> tuple[dict[str, str], int]:
        """Delete booking resource

        :param booking_id: id of the booking resource to delete
        :raise HTTPException: if given booking id does not exist
        :return: tuple of response json and status code
        """
        BookingDAO.get_by_id(booking_id)
        BookingDAO.delete(booking_id)
        return {"message": "Booking deleted successfully"}, codes.ok

    @staticmethod
    def update(booking_id: int) -> tuple[dict | Response, int]:
        """Update booking resource

        Validate and load update booking request json using booking schema.
        Check for existence of user id, booking status id, product id any was
        provided. Create booking model using Data Access Object.

        :raise HTTPException: raise if:
          - there are validation errors with create booking request json
          - given user id does not exist
          - given booking status id does not exist
          - given product id does not exist
        :return: tuple of response json and status code
        """
        try:
            booking_model = BookingDAO.get_by_id(booking_id)
            old_booking_data = booking_schema.dump(booking_model)
            update_booking_request_json = request.get_json()
            old_booking_data.update(update_booking_request_json)
            updated_booking_data = booking_schema.load(old_booking_data)
            BookingService.validate_create_or_update_booking_request(update_booking_request_json)
            BookingDAO.update(updated_booking_data)
            return booking_schema.dump(updated_booking_data), codes.ok
        except ValidationError as error:
            return jsonify(detail=str(error), status=codes.bad_request), codes.bad_request
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=codes.bad_request), codes.bad_request

    @staticmethod
    def validate_create_or_update_booking_request(create_or_update_booking_request_json: dict) -> None:
        """Validate request json to create or update booking resource

        :param create_or_update_booking_request_json:
        :raise HTTPException: raise if:
          - booking status id was provided, but it does not exist
          - user id was provided, but it does not exist
          - product id was provided, but it does not exist
        """
        if booking_status_id_to_validate := create_or_update_booking_request_json.get("status_id"):
            BookingStatusDAO.get_by_id(booking_status_id_to_validate)
        if user_id_to_validate := create_or_update_booking_request_json.get("user_id"):
            UserDAO.get_by_id(user_id_to_validate)
        if product_id_to_validate := create_or_update_booking_request_json.get("product_id"):
            ProductDAO.get_by_id(product_id_to_validate)
