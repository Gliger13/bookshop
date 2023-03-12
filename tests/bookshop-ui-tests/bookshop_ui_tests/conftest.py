"""Pytest conftest file to import all common fixtures and hooks for API tests"""
from bookshop_test_framework.fixtures.config.config import *
from bookshop_test_framework.fixtures.pages.user import *
from bookshop_test_framework.fixtures.pages.driver import *
from bookshop_test_framework.fixtures.pages.product import *
from bookshop_test_framework.fixtures.data.faker import *
from bookshop_test_framework.hooks.pytest_configure import *
