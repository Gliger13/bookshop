"""Store Item validation forms

Module contains UI input validation forms for store item related actions.
"""
from functools import cached_property

from flask_wtf import FlaskForm
from wtforms import IntegerField, validators

from bookshop_app.forms._base import BaseForm, FieldProtocol

__all__ = [
    "CreateStoreItemForm",
    "UpdateStoreItemForm",
    "DeleteStoreItemForm"
]


class StoreItemForm:
    """Form describes all store item properties"""

    id = FieldProtocol(label="ID", validators=[])
    product_id = FieldProtocol(label="Product ID", validators=[])
    available_quantity = FieldProtocol(label="Available", validators=[])
    booked_quantity = FieldProtocol(label="Booked", validators=[])
    sold_quantity = FieldProtocol(label="Sold", validators=[])


class CreateStoreItemForm(FlaskForm, BaseForm):
    """Input validation form for creating a store item"""

    __base = StoreItemForm

    product_id = IntegerField(__base.product_id.label, [validators.input_required(), *__base.product_id.validators])
    available_quantity = IntegerField(__base.available_quantity.label,
                                      [validators.optional(), *__base.available_quantity.validators])
    booked_quantity = IntegerField(__base.booked_quantity.label,
                                   [validators.optional(), *__base.booked_quantity.validators])
    sold_quantity = IntegerField(__base.sold_quantity.label,
                                 [validators.optional(), *__base.sold_quantity.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["product_id", "available_quantity", "booked_quantity", "sold_quantity"]


class UpdateStoreItemForm(FlaskForm, BaseForm):
    """Input validation form for updating a store item"""

    __base = StoreItemForm

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.id.validators])
    product_id = IntegerField(__base.product_id.label, [validators.optional(), *__base.product_id.validators])
    available_quantity = IntegerField(__base.available_quantity.label,
                                      [validators.optional(), *__base.available_quantity.validators])
    booked_quantity = IntegerField(__base.booked_quantity.label,
                                   [validators.optional(), *__base.booked_quantity.validators])
    sold_quantity = IntegerField(__base.sold_quantity.label,
                                 [validators.optional(), *__base.sold_quantity.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["id", "product_id", "available_quantity", "booked_quantity", "sold_quantity"]


class DeleteStoreItemForm(FlaskForm, BaseForm):
    """Input validation form for deleting a store item"""

    __base = StoreItemForm

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.id.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["id"]
