"""Base async API class"""
from abc import ABCMeta

from aiohttp import ClientSession


class BaseApi(metaclass=ABCMeta):
    """Base async API"""

    __slots__ = ("_session",)

    def __init__(self, session: ClientSession):
        """Initialize Async Base API with given session

        :param session: async session to use for all requests
        """
        self._session = session
