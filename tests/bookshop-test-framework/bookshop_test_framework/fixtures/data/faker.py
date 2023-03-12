"""Faker fixtures

Module contains fixtures that controls faker behavior.
"""
import logging
from random import randrange

import pytest

__all__ = ["faker_seed"]


@pytest.fixture(autouse=True)
def faker_seed() -> int:
    """Return faker random seed"""
    random_number = randrange(100000)
    logging.info("Faker configured with the random seed %s", random_number)
    return random_number
