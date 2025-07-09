from django.db import models
from django.conf import settings

class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    MARITAL_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    )

    MS_TYPE_CHOICES = (
        ('relapsing_remitting', 'Relapsing Remitting'),
        ('primary_progressive', 'Primary Progressive'),
        ('secondary_progressive', 'Secondary Progressive'),
        ('progressive_relapsing', 'Progressive Relapsing'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    national_id = models.CharField(max_length=50, unique=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    ms_type = models.CharField(max_length=30, choices=MS_TYPE_CHOICES)

    def __str__(self):
        return f"Patient: {self.user.phone_number} - {self.national_id}"
