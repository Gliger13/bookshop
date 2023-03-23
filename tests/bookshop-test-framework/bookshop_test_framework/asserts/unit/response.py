"""Unit tests response asserts"""
from collections import namedtuple
from typing import Iterable
from typing import Protocol

from requests import codes

from bookshop_test_framework.tools.soft_assert.soft_assert import expect
from bookshop_test_framework.tools.test_results import ApiTestResult

SimpleResponse = namedtuple("SimpleResponse", ("endpoint", "protocol", "status_code"))


class LikeResponse(Protocol):
    """Any response like object with basic response fields"""

    endpoint: str
    protocol: str
    status_code: int


def soft_check_response_status_code(response, expected_status_codes: int | Iterable[int] = codes.ok) -> bool:
    """Check response status code is the same as expected

    :param response: response with actual status code to check
    :param expected_status_codes: expected response status code or codes
    """
    actual_status_code = response.status_code
    expected_codes = {expected_status_codes} if isinstance(expected_status_codes, int) else set(expected_status_codes)
    expected_result_msg = f"Any of {expected_codes}" if len(expected_codes) > 1 else expected_status_codes
    return expect(
        actual_status_code in expected_codes,
        ApiTestResult(
            check_message="Check response status code is the same as expected",
            method=response.protocol,
            endpoint=response.endpoint,
            actual_result=actual_status_code,
            expected_result=expected_result_msg,
        ),
    )
