"""ORM User Schemas"""
from marshmallow import validate, validates, ValidationError

from bookshop_app.database.database import db
from bookshop_app.dependencies import ma
from bookshop_app.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    """User schema"""

    class Meta:
        model = UserModel
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    login = ma.auto_field()

    role_id = ma.auto_field()

    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    address = ma.auto_field()

    @staticmethod
    def validate_password(password: str) -> None:
        """Validate user password

        :param password: password to validate
        :raise ValidationError: if something wrong with the given password
        """
        if not password:
            raise ValidationError("Password must be not empty")
        validate.Length(min=8, max=256)(password)

    @validates("name")
    def validate_name(self, name: str) -> None:
        """Validate user password

        :param name: name to validate
        :raise ValidationError: if something wrong with the given name
        """
        if name:
            validate.Length(min=2, max=256)(name)

    @validates("email")
    def validate_email(self, email: str) -> None:
        """Validate user password

        :param email: email to validate
        :raise ValidationError: if something wrong with the given email
        """
        validate.Email()(email)

    @validates("login")
    def validate_login(self, login: str) -> None:
        """Validate user password

        :param login: login to validate
        :raise ValidationError: if something wrong with the given login
        """
        validate.Length(min=2, max=256)(login)

    @validates("phone")
    def validate_phone(self, phone: str) -> None:
        """Validate user password

        :param phone: phone to validate
        :raise ValidationError: if something wrong with the given phone
        """
        if phone:
            validate.Regexp(regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")(phone)

    @validates("address")
    def validate_address(self, address: str) -> None:
        """Validate user password

        :param address: address to validate
        :raise ValidationError: if something wrong with the given address
        """
        if address:
            validate.Length(min=2, max=256)(address)
