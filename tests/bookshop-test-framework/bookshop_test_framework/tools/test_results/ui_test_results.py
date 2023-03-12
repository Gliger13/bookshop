"""UI Test Result model"""
from dataclasses import dataclass
from typing import Any

from .base_test_result import TestResult
from .test_result_attributes import TestResultAttributes


@dataclass(eq=False, frozen=True, kw_only=True, slots=True)
class UiTestResult(TestResult):
    """Responsible for containing UI test result attributes

    :param check_message: message of the test check
    :param endpoint: endpoint - ('/api/user')
    :param actual_result: actual result for check
    :param expected_result: expected result for check
    :param difference: difference between actual and expected result if needed
    """

    check_message: str = ""
    endpoint: str = ""
    expected_result: Any = True
    actual_result: Any = False
    difference: Any = ""

    def result(self) -> dict[str, str]:
        """Return result attribute name and string result value as dict"""
        return {
            TestResultAttributes.CHECK_MESSAGE: str(self.check_message),
            TestResultAttributes.ENDPOINT: str(self.endpoint),
            TestResultAttributes.ACTUAL_RESULT: str(self.actual_result),
            TestResultAttributes.EXPECTED_RESULT: str(self.expected_result),
            TestResultAttributes.DIFFERENCE: str(self.difference),
        }
