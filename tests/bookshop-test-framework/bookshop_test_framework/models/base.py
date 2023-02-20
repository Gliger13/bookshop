"""Base models for all test framework models"""
from abc import ABCMeta
from dataclasses import dataclass
from typing import Mapping


@dataclass
class UpdatableDataModel(metaclass=ABCMeta):
    """Provides `update` method for all inheritance"""

    def update(self, new_attributes: Mapping) -> None:
        """Update fields with the given attributes

        Update dataclass instance fields with the given attributes. Ignore
        extra one.

        :param new_attributes: map of field items to set
        """
        for key, value in new_attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)
