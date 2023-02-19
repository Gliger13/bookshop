"""Test results packages that provides different test results models"""
from .api_test_result import ApiTestResult
from .base_test_result import TestResult
from .resource_test_result import ResourceTestResult
from .test_result_attributes import TestResultAttributes

__all__ = [
    "TestResult",
    "ApiTestResult",
    "ResourceTestResult",
    "TestResultAttributes",
]
