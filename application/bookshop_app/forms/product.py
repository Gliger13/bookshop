"""Product validation forms

Module contains UI input validation forms for product related actions.
"""
from functools import cached_property

from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, IntegerField, StringField, TextAreaField, validators

from bookshop_app.forms._base import BaseForm, FieldProtocol

__all__ = [
    "CreateProductForm",
    "UpdateProductForm",
    "DeleteProductForm"
]


class ProductForm:
    """Base product form with common labels and validators"""

    id = FieldProtocol(label="ID", validators=[])
    name = FieldProtocol(label="Name", validators=[validators.length(min=2, max=256)])
    author = FieldProtocol(label="Author", validators=[validators.length(min=2, max=256)])
    description = FieldProtocol(label="Description", validators=[])
    price = FieldProtocol(label="Price", validators=[validators.number_range(min=0.01)])
    image = FieldProtocol(label="Image File", validators=[])


class CreateProductForm(FlaskForm, BaseForm):
    """Input validation form for creating a product"""

    __base = ProductForm

    name = StringField(__base.name.label, [validators.input_required(), *__base.name.validators])
    author = StringField(__base.author.label, [validators.input_required(), *__base.author.validators])
    description = TextAreaField(__base.description.label, [validators.input_required(), *__base.description.validators])
    price = FloatField(__base.price.label, [validators.input_required(), *__base.price.validators])
    image = FileField(__base.image.label, [validators.optional(), *__base.image.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["name", "author", "description", "price", "image"]


class UpdateProductForm(FlaskForm, BaseForm):
    """Input validation form for updating a product"""

    __base = ProductForm

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.id.validators])
    name = StringField(__base.name.label, [validators.optional(), *__base.name.validators])
    author = StringField(__base.author.label, [validators.optional(), *__base.author.validators])
    description = TextAreaField(__base.description.label, [validators.optional(), *__base.description.validators])
    price = FloatField(__base.price.label, [validators.optional(), *__base.price.validators])
    image = FileField(__base.image.label, [validators.optional(), *__base.image.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["id", "name", "author", "description", "price", "image"]


class DeleteProductForm(FlaskForm, BaseForm):
    """Input validation form for deleting a product"""

    __base = ProductForm

    id = IntegerField(__base.id.label, [validators.input_required(), *__base.name.validators])

    @cached_property
    def field_names(self) -> list[str]:
        """All required and optional field names"""
        return ["id"]
