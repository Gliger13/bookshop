from dataclasses import dataclass
from typing import Optional

from bookshop_test_framework.models.base import UpdatableDataModel


@dataclass(kw_only=True, slots=True)
class StoreItem(UpdatableDataModel):
    id: Optional[int] = None

    product_id: Optional[int] = None

    available_quantity: Optional[int] = None
    booked_quantity: Optional[int] = None
    sold_quantity: Optional[int] = None
