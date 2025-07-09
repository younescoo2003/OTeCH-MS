from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_id', 'birthdate', 'gender', 'marital_status', 'ms_type')
    search_fields = ('user__phone_number', 'national_id')
