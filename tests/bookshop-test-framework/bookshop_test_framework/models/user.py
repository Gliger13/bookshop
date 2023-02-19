from dataclasses import dataclass
from typing import Optional

from bookshop_test_framework.models.base import UpdatableDataModel


@dataclass(kw_only=True, slots=True)
class User(UpdatableDataModel):
    id: Optional[int] = None
    login: Optional[str] = None
    password: Optional[str] = None

    role_id: Optional[int] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None

    @property
    def auth(self) -> tuple[Optional[str], Optional[str]]:
        if not self.login or not self.password:
            raise ValueError("Can not get user authentication tuple. One of the creds is empty")
        return self.login, self.password
