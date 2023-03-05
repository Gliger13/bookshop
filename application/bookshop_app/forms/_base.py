from abc import abstractmethod
from collections import namedtuple
from functools import cached_property

FieldProtocol = namedtuple("FieldProtocol", ["label", "validators"])


class BaseForm:
    @cached_property
    @abstractmethod
    def field_names(self) -> list[str]:
        """All required and optional field names"""
