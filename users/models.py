from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from utils.validations import phone_regex, name_regex

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[phone_regex])
    first_name = models.CharField(max_length=30, validators=[name_regex])
    last_name = models.CharField(max_length=30, validators=[name_regex])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(default=timezone.now)
    ROLE_CHOICES = (
        ('not_registered', 'Not Registered'),
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('therapist', 'Therapist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='not_registered')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
