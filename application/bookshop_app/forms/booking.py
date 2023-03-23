"""Booking validation forms

Module contains UI input validation forms for booking related actions.
"""
from functools import cached_property

from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import StringField
from wtforms import validators

from bookshop_app.forms._base import BaseForm

__all__ = ["BookProductForm"]


class BookProductForm(FlaskForm, BaseForm):
    """Form for booking a product by id"""

    product_id = HiddenField(label="")
    user_id = HiddenField(label="")
    delivery_address = StringField("Delivery Address", validators=[validators.length(min=1, max=256)])
    quantity = IntegerField("Quantity", default=1, validators=[validators.length(min=1)])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["product_id", "user_id", "delivery_address", "quantity"]
