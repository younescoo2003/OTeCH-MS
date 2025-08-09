import re
from uuid import UUID
from django.core.exceptions import ValidationError


def validate_iranian_national_id(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError('کد ملی باید ۱۰ رقم باشد.')

    return value

def validate_name(value):
    if not re.match(r'^[a-zA-Z\u0600-\u06FF\s]+$', value):
        raise ValidationError('نام وارد شده معتبر نمی باشد.')
    return value


def validate_address(value):
    if not re.match(r'^[a-zA-Z0-9\u0600-\u06FF\s,.-]+$', value):
        raise ValidationError('آدرس وارد شده معتبر نمی باشد.')
    return value


def validate_uuid(value):
    try:
        UUID(str(value))
        return value
    except ValueError:
        raise ValidationError('مقدار وارد شده یک UUID معتبر نمی باشد.')


def validate_iranian_phone_number(value):
    if not re.match(r'^(\+989)\d{9}$', value):
        raise ValidationError('شماره تلفن وارد شده معتبر نمی باشد.')
    return value