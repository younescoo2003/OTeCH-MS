from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
import uuid

def validate_national_id(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError('National ID must be 10 digits')

def validate_name(value):
    if len(value) > 100:
        raise ValidationError('Name cannot exceed 100 characters')
    if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z\s]+$', value):
        raise ValidationError('Name can only contain letters and spaces')

def validate_address(value):
    if len(value) > 255:
        raise ValidationError('Address cannot exceed 255 characters')
    if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9\-\s.,#]+$', value):
        raise ValidationError('Address contains invalid characters')

def validate_uuid(value):
    try:
        uuid_obj = uuid.UUID(str(value))
        if str(uuid_obj) != str(value):
            raise ValueError
    except (ValueError, TypeError, AssertionError):
        raise ValidationError("invalid uuid")


national_id_regex = RegexValidator(
    regex=r'^\d{10}$',
    message='National ID must be 10 digits'
)

phone_regex = RegexValidator(
    regex=r'^(\+98|0)?9\d{9}$',
    message='Phone number must be a valid Iranian mobile number'
)

name_regex = RegexValidator(
    regex=r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z\s]+$',
    message='Name can only contain letters and spaces'
)

address_regex = RegexValidator(
    regex=r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9\-\s.,#]+$',
    message='Address contains invalid characters'
)