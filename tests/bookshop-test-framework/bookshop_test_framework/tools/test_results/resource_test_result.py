"""Resource Test Result model"""
from dataclasses import dataclass
from typing import Any

from .base_test_result import TestResult
from .test_result_attributes import TestResultAttributes


@dataclass(eq=False, frozen=True, kw_only=True, slots=True)
class ResourceTestResult(TestResult):
    """Responsible for containing test result attributes

    :param check_message: message of the test check
    :param resource_type: resource type, e.g. 'channel'
    :param resource_name: name of the resource
    :param resource_id: id of the resource
    :param actual_result: actual result for check
    :param expected_result: expected result for check
    :param difference: difference between actual and expected result if needed
    """

    check_message: str = ""
    resource_type: str = ""
    resource_name: str = ""
    resource_id: int | str = ""
    expected_result: Any = True
    actual_result: Any = False
    difference: Any = ""

    def result(self) -> dict[str, str]:
        """Return result attribute name and string result value as dict"""
        return {
            TestResultAttributes.CHECK_MESSAGE: str(self.check_message),
            TestResultAttributes.RESOURCE_TYPE: str(self.resource_type),
            TestResultAttributes.RESOURCE_NAME: str(self.resource_name),
            TestResultAttributes.RESOURCE_ID: str(self.resource_id),
            TestResultAttributes.ACTUAL_RESULT: str(self.actual_result),
            TestResultAttributes.EXPECTED_RESULT: str(self.expected_result),
            TestResultAttributes.DIFFERENCE: str(self.difference),
        }
