"""UI validation forms package

Package contains modules with all UI input validation forms for all resources.
"""
from . import authentication
from . import booking
from . import product
from . import store_item

__all__ = ["authentication", "booking", "product", "store_item"]
