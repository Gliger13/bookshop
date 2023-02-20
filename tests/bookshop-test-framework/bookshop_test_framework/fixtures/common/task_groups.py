"""Async task groups

Module contains fixtures that provide async task groups for different tests
scopes.
"""
from asyncio import TaskGroup

import pytest


@pytest.fixture(scope="session")
def http_task_group() -> TaskGroup:
    """Async task group for grouping http request tasks

    :return: async task group
    """
    return TaskGroup()
