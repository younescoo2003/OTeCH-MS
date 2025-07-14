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
        extra_kwargs = {
            'user': {'help_text': 'The user account associated with this patient'},
            'modified_at': {'help_text': 'Timestamp of last modification'},
            'last_modified_by': {'help_text': 'User who last modified this record'},
            'national_id': {'help_text': 'National identification number'},
            'birthdate': {'help_text': 'Patient date of birth (YYYY-MM-DD)'},
            'gender': {'help_text': 'Patient gender (M/F/Other)'},
            'marital_status': {'help_text': 'Marital status (e.g., single, married)'},
            'education_level': {'help_text': 'Highest level of education completed'},
            'current_occupation': {'help_text': 'Current job or occupation'},
            'years_employed': {'help_text': 'Number of years in current occupation'},
            'address': {'help_text': 'Full residential address'},
            'emergency_contact_name': {'help_text': 'Emergency contact full name'},
            'emergency_contact_phone': {'help_text': 'Emergency contact phone number'},
            'emergency_contact_relationship': {'help_text': 'Relationship to patient'},
            'ms_type': {'help_text': 'Type of Multiple Sclerosis (e.g., RRMS, PPMS)'},
            'ms_diagnosis_date': {'help_text': 'Date of MS diagnosis (YYYY-MM-DD)'},
            'number_of_relapses': {'help_text': 'Total number of relapses experienced'},
            'relapse_dates_and_areas': {'help_text': 'Dates and affected areas of relapses'},
            'family_medical_history': {'help_text': 'Relevant family medical history'},
            'caregiver_diseases': {'help_text': 'Diseases present in caregiver(s)'},
            'drug_allergies': {'help_text': 'Known drug allergies'},
            'food_allergies': {'help_text': 'Known food allergies'},
            'physiotherapy_received': {'help_text': 'History of physiotherapy received'},
            'occupational_therapy_received': {'help_text': 'History of occupational therapy received'},
            'mobility_aids_used': {'help_text': 'Mobility aids currently used'},
            'therapist_cooperation_level': {'help_text': 'Patient cooperation level with therapists'},
            'motor_status': {'help_text': 'Current motor function status'},
            'muscle_strength': {'help_text': 'Assessment of muscle strength'},
            'balance': {'help_text': 'Balance assessment results'},
            'walking_ability': {'help_text': 'Walking ability assessment'},
            'adl_activities': {'help_text': 'Activities of Daily Living assessment'},
            'iadl_activities': {'help_text': 'Instrumental Activities of Daily Living assessment'},
            'cognitive_status': {'help_text': 'Cognitive function assessment'},
            'speech_status': {'help_text': 'Speech ability assessment'},
            'swallowing_status': {'help_text': 'Swallowing function assessment'},
            'fatigue_level': {'help_text': 'Level of fatigue experienced'},
            'psychological_status': {'help_text': 'Psychological/mental health assessment'},
            'living_environment': {'help_text': 'Description of living environment'},
            'equipment_used_daily': {'help_text': 'Equipment used in daily activities'},
            'equipment_used_work': {'help_text': 'Equipment used for work activities'},
            'environmental_modifications_needed': {'help_text': 'Required home/work modifications'},
            'assistive_devices_needed': {'help_text': 'Required assistive devices'},
            'short_term_goals': {'help_text': 'Short-term therapeutic goals'},
            'long_term_goals': {'help_text': 'Long-term therapeutic goals'},
            'patient_personal_goals': {'help_text': 'Patient personal rehabilitation goals'},
            'therapist_team_goals': {'help_text': 'Therapist team goals for patient'},
            'goal_timeline': {'help_text': 'Timeline for achieving goals'},
            'recommended_exercises': {'help_text': 'Recommended therapeutic exercises'},
            'fatigue_management_techniques': {'help_text': 'Recommended fatigue management techniques'},
            'environmental_adaptation': {'help_text': 'Recommended environmental adaptations'},
            'family_education': {'help_text': 'Family education topics'},
            'caregiver_education': {'help_text': 'Caregiver education topics'},
            'session_scheduling': {'help_text': 'Therapy session schedule'},
            'progress_monitoring': {'help_text': 'Progress monitoring plan'}
        }


class PatientRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        validators=[name_regex],
        help_text="Patient's first name"
    )
    last_name = serializers.CharField(
        required=True,
        validators=[name_regex],
        help_text="Patient's last name"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Account password (min 8 characters)"
    )
    temp_token = serializers.CharField(
        required=True,
        validators=[validate_uuid],
        help_text="Temporary token from OTP verification"
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Phone number in international format (+989123456789)"
    )
    national_id = serializers.CharField(
        required=True,
        help_text="National identification number"
    )
    birthdate = serializers.DateField(
        required=True,
        help_text="Date of birth (YYYY-MM-DD)"
    )
    gender = serializers.ChoiceField(
        choices=Patient.GENDER_CHOICES,
        required=True,
        help_text="Gender: M (Male), F (Female)"
    )
    marital_status = serializers.ChoiceField(
        choices=Patient.MARITAL_STATUS_CHOICES,
        required=True,
        help_text="Marital status: S (Single), M (Married), D (Divorced), W (Widowed)"
    )
    ms_type = serializers.ChoiceField(
        choices=Patient.MS_TYPE_CHOICES,
        required=True,
        help_text="Type of Multiple Sclerosis: RRMS, PPMS, SPMS, PRMS"
    )
    education_level = serializers.CharField(
        required=True,
        help_text="Highest education level completed"
    )
    address = serializers.CharField(
        required=True,
        help_text="Full residential address"
    )
    emergency_contact_name = serializers.CharField(
        required=True,
        help_text="Emergency contact full name"
    )
    emergency_contact_phone = serializers.CharField(
        required=True,
        validators=[phone_regex],
        help_text="Emergency contact phone number"
    )
    emergency_contact_relationship = serializers.CharField(
        required=True,
        help_text="Relationship to patient (e.g., spouse, parent)"
    )
    current_occupation = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text="Current job or occupation (optional)"
    )
    years_employed = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0,
        help_text="Years in current occupation (optional)"
    )

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
            'current_occupation',
            'years_employed',
        ]

    def validate(self, data):
        """
        Validate temporary token and phone number verification status.
        Also validates registration data through RegisterSerializer.
        """
        reg = RegisterSerializer(data=data)
        if reg.is_valid():
            # Check if phone number has been verified
            cached_token = auth_cache.get(f'verified_{data['phone_number']}')
            if cached_token is None:
                raise serializers.ValidationError('Phone number is not verified')
            
            # Validate temporary token matches cached token
            if cached_token != data['temp_token'] or not data['temp_token']:
                raise serializers.ValidationError('Invalid temporary token')
        else:
            raise serializers.ValidationError(reg.errors)

        return data

    def create(self, validated_data):
        """
        Create a new Patient and associated User account.
        Deletes the verification token from cache after successful registration.
        """
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

        # Clear verification token from cache after successful registration
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
