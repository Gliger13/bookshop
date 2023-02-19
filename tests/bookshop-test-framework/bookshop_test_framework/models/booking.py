from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bookshop_test_framework.models.base import UpdatableDataModel


@dataclass(kw_only=True, slots=True)
class Booking(UpdatableDataModel):
    id: Optional[int] = None

    product_id: Optional[int] = None
    user_id: Optional[int] = None
    status_id: Optional[int] = None

    delivery_address: Optional[str] = None
    quantity: Optional[int] = None

    delivery_date: Optional[datetime] = None
    delivery_time: Optional[datetime] = None
