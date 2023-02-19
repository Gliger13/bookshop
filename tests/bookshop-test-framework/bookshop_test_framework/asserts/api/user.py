"""Asserts for User API"""
from dataclasses import asdict

from aiohttp import ClientResponse
from requests import codes

from bookshop_test_framework.asserts.api.response import soft_check_response_body_is_json, \
    soft_check_response_json_attributes, soft_check_response_json_is_not_empty, soft_check_response_status_code
from bookshop_test_framework.models.user import User


async def soft_check_create_user_attributes(user_response: ClientResponse, expected_user: User) -> bool:
    """Soft check given create user response json has all expected attributes

    :param user_response: create user response with actual user attributes
    :param expected_user: expected user model
    :return: True if create user response has all expected attrs else False
    """
    ignore_user_fields = {"password", "id"}
    expected_user_attributes = {name: value for name, value in asdict(expected_user).items()
                                if name not in ignore_user_fields}
    return await soft_check_response_json_attributes(user_response, expected_user_attributes,
                                                     ignore_actual_fields={"id"})


async def soft_check_user_attributes(user_response: ClientResponse, expected_user: User) -> bool:
    """Soft check given update user response json has all expected attributes

    :param user_response: get or update user response with actual attributes
    :param expected_user: expected user model
    :return: True if create user response has all expected attrs else False
    """
    ignore_user_fields = {"password"}
    expected_user_attributes = {name: value for name, value in asdict(expected_user).items()
                                if name not in ignore_user_fields}
    return await soft_check_response_json_attributes(user_response, expected_user_attributes)


async def check_create_user_response(create_user_response: ClientResponse, expected_user: User) -> bool:
    """Check create user response has expected code and body

    :param create_user_response: create user response with actual attributes
    :param expected_user: expected user model
    :return: True if create user response is the same as expected else False
    """
    return all((
        soft_check_response_status_code(create_user_response, codes.created),
        await soft_check_response_body_is_json(create_user_response),
        await soft_check_response_json_is_not_empty(create_user_response),
        await soft_check_create_user_attributes(create_user_response, expected_user),
    ))


async def check_update_user_response(update_user_response: ClientResponse, expected_user: User) -> bool:
    """Check update user response has expected code and body

    :param update_user_response: create user response with actual attributes
    :param expected_user: expected user model
    :return: True if update user response is the same as expected else False
    """
    return all((
        soft_check_response_status_code(update_user_response, codes.ok),
        await soft_check_response_body_is_json(update_user_response),
        await soft_check_response_json_is_not_empty(update_user_response),
        await soft_check_user_attributes(update_user_response, expected_user),
    ))


async def check_get_user_response(get_user_response: ClientResponse, expected_user: User) -> bool:
    """Check get user response has expected code and body

    :param get_user_response: get user response with actual attributes
    :param expected_user: expected user model
    :return: True if update user response is the same as expected else False
    """
    return all((
        soft_check_response_status_code(get_user_response, codes.ok),
        await soft_check_response_body_is_json(get_user_response),
        await soft_check_response_json_is_not_empty(get_user_response),
        await soft_check_user_attributes(get_user_response, expected_user),
    ))
