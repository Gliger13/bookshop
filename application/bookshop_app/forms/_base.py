"""Base UI validation forms

Module contains common class and methods for all project UI validation forms.
"""
from abc import abstractmethod
from collections import namedtuple
from functools import cached_property
from typing import Collection

FieldProtocol = namedtuple("FieldProtocol", ["label", "validators"])


class BaseForm:
    """Base UI input validation

    Defines general interfaces for all forms
    """

    @cached_property
    @abstractmethod
    def field_names(self) -> Collection[str]:
        """All required and optional field names"""
        raise NotImplementedError()
