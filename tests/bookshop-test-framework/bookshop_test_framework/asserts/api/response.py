"""Module with asserts for request responses"""
import logging
from json import JSONDecodeError
from typing import Collection, Iterable, Optional, Union

from aiohttp import ClientResponse, ContentTypeError
from deepdiff import DeepDiff
from requests import codes

from bookshop_test_framework.tools.soft_assert.soft_assert import expect
from bookshop_test_framework.tools.test_results.api_test_result import ApiTestResult


def soft_check_response_status_code(
    response: ClientResponse, expected_status_codes: Union[int, Iterable[int]] = codes.ok
) -> bool:
    """Check response status code is the same as expected

    :param response: response with actual status code to check
    :param expected_status_codes: expected response status code or codes
    """
    actual_status_code = response.status
    expected_codes = {expected_status_codes} if isinstance(expected_status_codes, int) else set(expected_status_codes)
    expected_result_msg = f"Any of {expected_codes}" if len(expected_codes) > 1 else expected_status_codes
    return expect(
        actual_status_code in expected_codes,
        ApiTestResult(
            check_message="Check response status code is the same as expected",
            method=response.method,
            endpoint=response.url.path,
            actual_result=actual_status_code,
            expected_result=expected_result_msg,
        ),
    )


async def soft_check_response_body_is_json(response: ClientResponse) -> bool:
    """Check response has body and body is json

    :param response: response with body to check
    """
    try:
        response_json = await response.json()
    except (ContentTypeError, JSONDecodeError) as json_error:
        logging.warning("Can not get json from the response body - %s", json_error)
        response_json = None

    return expect(
        response_json is not None,
        ApiTestResult(
            check_message="Check response has body in JSON format", method=response.method, endpoint=response.url.path
        ),
    )


async def soft_check_response_json_is_not_empty(response: ClientResponse) -> bool:
    """Check response has not empty json

    :param response: response with body to check
    """
    response_json = await response.json()
    return expect(
        response_json,
        ApiTestResult(
            check_message="Check response has not empty body JSON", method=response.method, endpoint=response.url.path
        ),
    )


async def soft_check_response_json_attributes(
    response: ClientResponse, expected_attributes: dict, *, ignore_actual_fields: Optional[Collection[str]] = None
) -> bool:
    """Check response has body and body is json

    :param response: response with body to check
    :param expected_attributes: expected response json attributes
    :param ignore_actual_fields: remove specific attributes in response
    :return: True if the response json is the same as given expected else False
    """
    if not ignore_actual_fields:
        ignore_actual_fields = []

    response_json = await response.json()
    logging.info(response_json)
    difference = DeepDiff(response_json, expected_attributes, exclude_paths=ignore_actual_fields, view="text")
    pretty_difference = "\n".join({str(item) for item in difference.to_dict().items()})
    return expect(
        not difference,
        ApiTestResult(
            check_message="Check response has expected attributes",
            method=response.method,
            endpoint=response.url.path,
            difference=pretty_difference,
        ),
    )
