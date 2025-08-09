from rest_framework import serializers
from .models import Patient
from users.serializers import UserSerializer

class PatientListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'national_id',
            'birthdate',
            'gender',
            'marital_status',
            'education_level',
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'years_employed',
            'current_occupation',
            'ms_type',
            'ms_diagnosis_date',
        ]
        extra_kwargs = {
            'national_id': {'help_text': 'The national ID of the patient.'},
            'birthdate': {'help_text': 'The birthdate of the patient.'},
            'gender': {'help_text': 'The gender of the patient.'},
            'marital_status': {'help_text': 'The marital status of the patient.'},
            'education_level': {'help_text': 'The education level of the patient.'},
            'address': {'help_text': 'The address of the patient.'},
            'emergency_contact_name': {'help_text': 'The name of the emergency contact.'},
            'emergency_contact_phone': {'help_text': 'The phone number of the emergency contact.'},
            'emergency_contact_relationship': {'help_text': 'The relationship of the emergency contact to the patient.'},
            'years_employed': {'help_text': 'The number of years the patient has been employed.'},
            'current_occupation': {'help_text': 'The current occupation of the patient.'},
            'ms_type': {'help_text': 'The type of MS the patient has.'},
            'ms_diagnosis_date': {'help_text': 'The date the patient was diagnosed with MS.'},
        }
