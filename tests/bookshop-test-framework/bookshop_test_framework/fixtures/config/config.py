"""Test config related fixtures"""
import pytest as pytest

from bookshop_test_framework.config.config import Config
from bookshop_test_framework.config.config import get_config


@pytest.fixture(scope="session")
def config() -> Config:
    """Initialize and return config for the current environment"""
    return get_config()
