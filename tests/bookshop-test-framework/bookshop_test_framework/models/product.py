from dataclasses import dataclass
from typing import Optional

from bookshop_test_framework.models.base import UpdatableDataModel


@dataclass(kw_only=True, slots=True)
class Product(UpdatableDataModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
