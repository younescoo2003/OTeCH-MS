from django.core.cache import caches
from rest_framework import serializers
from .models import Patient, PatientProgressMonitoring, PatientMedicine
from users.serializers import RegisterSerializer, UserSerializer
from utils.validations import name_regex, phone_regex, validate_uuid

auth_cache = caches['auth']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'user',
            'modified_at',
            'last_modified_by',
            'national_id',
            'birthdate',
            'gender',
            'marital_status',
            'education_level',
            'current_occupation',
            'years_employed',
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',
            'ms_type',
            'ms_diagnosis_date',
            'number_of_relapses',
            'relapse_dates_and_areas',
            'family_medical_history',
            'caregiver_diseases',
            'drug_allergies',
            'food_allergies',
            'physiotherapy_received',
            'occupational_therapy_received',
            'mobility_aids_used',
            'therapist_cooperation_level',
            'motor_status',
            'muscle_strength',
            'balance',
            'walking_ability',
            'adl_activities',
            'iadl_activities',
            'cognitive_status',
            'speech_status',
            'swallowing_status',
            'fatigue_level',
            'psychological_status',
            'living_environment',
            'equipment_used_daily',
            'equipment_used_work',
            'environmental_modifications_needed',
            'assistive_devices_needed',
            'short_term_goals',
            'long_term_goals',
            'patient_personal_goals',
            'therapist_team_goals',
            'goal_timeline',
            'recommended_exercises',
            'fatigue_management_techniques',
            'environmental_adaptation',
            'family_education',
            'caregiver_education',
            'session_scheduling',
            'progress_monitoring'
        ]


class PatientRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, validators=[name_regex])
    last_name = serializers.CharField(required=True, validators=[name_regex])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    temp_token = serializers.CharField(required=True, validators=[validate_uuid])
    phone_number = serializers.CharField(required=True, validators=[phone_regex])

    class Meta:
        model = Patient
        fields = [
            'national_id',
            'birthdate',
            'gender',
            'marital_status',
            'first_name',
            'last_name',
            'password',
            'temp_token',
            'phone_number',
            'ms_type',
            'education_level',
            'address',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relationship',

            # Not Required
            'current_occupation',
            'years_employed',
        ]

    def validate(self, data):
        reg = RegisterSerializer(data=data)
        if reg.is_valid():
            cached_token = auth_cache.get(f'verified_{data['phone_number']}')   
            if cached_token is None:
                raise serializers.ValidationError('Number is Not Verified')
            
            if cached_token != data['temp_token'] or not data['temp_token']:
                raise serializers.ValidationError('Invalid temp token')
        else:
            raise serializers.ValidationError(reg.errors)


        return data

    def create(self, validated_data):
        validated_data['role'] = 'patient'
        reg = RegisterSerializer(data=validated_data)
        if not reg.is_valid():
            raise serializers.ValidationError(reg.errors)
        user = reg.create(validated_data)

        patient = Patient.objects.create(
            user=user,
            national_id=validated_data['national_id'],
            birthdate=validated_data['birthdate'],
            gender=validated_data['gender'],
            marital_status=validated_data['marital_status'],
            ms_type=validated_data['ms_type'],
            education_level=validated_data['education_level'],
            address=validated_data['address'],
            emergency_contact_name=validated_data['emergency_contact_name'],
            emergency_contact_phone=validated_data['emergency_contact_phone'],
            emergency_contact_relationship=validated_data['emergency_contact_relationship'],
            current_occupation=validated_data.get('current_occupation', ''),
            years_employed=validated_data.get('years_employed', None),
        )

        auth_cache.delete(f'verified_{validated_data['phone_number']}')

        return patient

class PatientProgressMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProgressMonitoring
        fields = '__all__'

class PatientMedicineSerializer(serializers.ModelSerializer):
    dosage = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientMedicine
        fields = '__all__'
        read_only_fields = ('patient',)

    def get_dosage(self, obj):
        return f'{obj.dosage_amount}{obj.dosage_unit}'
