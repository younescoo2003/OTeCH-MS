from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from utils.validations import validate_iranian_phone_number, validate_name
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=100, validators=[validate_name])
    last_name = models.CharField(max_length=100, validators=[validate_name])
    
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=13,unique=True,validators=[validate_iranian_phone_number])
    is_registration_complete = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number