from django.db import models
from users.models import User

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
        ('RRMS', 'Relapsing Remitting'),
        ('PPMS', 'Primary Progressive'),
        ('SPMS', 'Secondary Progressive'),
        ('CIS', 'Clinically Isolated Syndrome'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='patient_profile')
    modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Personal Information
    national_id = models.CharField(max_length=50, unique=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    age = models.IntegerField()
    education_level = models.CharField(max_length=100)
    current_occupation = models.CharField(max_length=100, blank=True)
    years_employed = models.IntegerField(blank=True)
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)

    # Medical History
    ms_type = models.CharField(max_length=30, choices=MS_TYPE_CHOICES)
    ms_diagnosis_date = models.DateField(blank=True)
    number_of_relapses = models.IntegerField(blank=True)
    relapse_dates_and_areas = models.TextField(blank=True)
    family_medical_history = models.TextField(blank=True)
    caregiver_diseases = models.TextField(blank=True)
    drug_allergies = models.TextField(blank=True)
    food_allergies = models.TextField(blank=True)

    # Treatment and Rehabilitation History
    physiotherapy_received = models.TextField(blank=True)
    occupational_therapy_received = models.TextField(blank=True)
    mobility_aids_used = models.TextField(blank=True)
    therapist_cooperation_level = models.CharField(max_length=50, blank=True)

    # Functional Assessments
    motor_status = models.TextField(blank=True)
    muscle_strength = models.TextField(blank=True)
    balance = models.TextField(blank=True)
    walking_ability = models.TextField(blank=True)
    adl_activities = models.TextField(blank=True)
    iadl_activities = models.TextField(blank=True)
    cognitive_status = models.TextField(blank=True)
    speech_status = models.TextField(blank=True)
    swallowing_status = models.TextField(blank=True)
    fatigue_level = models.TextField(blank=True)
    psychological_status = models.TextField(blank=True)

    # Environmental Evaluation
    living_environment = models.TextField(blank=True)
    equipment_used_daily = models.TextField(blank=True)
    equipment_used_work = models.TextField(blank=True)
    environmental_modifications_needed = models.TextField(blank=True)
    assistive_devices_needed = models.TextField(blank=True)

    # Treatment Goals
    short_term_goals = models.TextField(blank=True)
    long_term_goals = models.TextField(blank=True)
    patient_personal_goals = models.TextField(blank=True)
    therapist_team_goals = models.TextField(blank=True)
    goal_timeline = models.TextField(blank=True)

    # Occupational Therapy Treatment Plan
    recommended_exercises = models.TextField(blank=True)
    fatigue_management_techniques = models.TextField(blank=True)
    environmental_adaptation = models.TextField(blank=True)
    family_education = models.TextField(blank=True)
    caregiver_education = models.TextField(blank=True)
    session_scheduling = models.TextField(blank=True)
    progress_monitoring = models.TextField(blank=True)


    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name} - {self.national_id}"

class PatientProgressMonitoring(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    performance_improvement = models.TextField()
    performance_loss = models.TextField()
    assessment_date = models.DateField()
    next_assessment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress Monitoring for {self.patient} on {self.assessment_date}"

class PatientMedicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    medicine_type = models.CharField(max_length=100)
    medicine_category = models.CharField(max_length=100)

    # Dosage and Administration
    dosage_amount = models.PositiveIntegerField()
    dosage_unit = models.CharField(max_length=50)
    frequency_per_day = models.PositiveIntegerField()
    frequency_description = models.TextField(blank=True)
    administration_route = models.CharField(max_length=100)
    administration_time = models.CharField(max_length=100)

    # Treatment Duration
    start_date = models.DateField()
    end_date = models.DateField()

    # Presciber Information
    prescriber_name = models.CharField(max_length=200)
    prescriber_specialty = models.CharField(max_length=100)
    prescription_date = models.DateField()
    prescription_number = models.CharField(max_length=100)

    # Medicine Purpose
    prescribed_for = models.CharField(max_length=200)
    purpose_description = models.TextField(blank=True)

    # Effectiveness and Response
    effectiveness_rating = models.PositiveSmallIntegerField(min=1, max=10)
    patient_response = models.CharField(max_length=200)
    response_notes = models.TextField(blank=True)

    # Side Effects
    has_side_effects = models.BooleanField()
    side_effect_severity = models.CharField(max_length=200, blank=True)
    side_effects = models.TextField(blank=True)

    # Status and History
    CURRENT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('discontinued', 'Discontinued'),
        ('paused', 'Paused'),
        ('completed', 'Completed')
    )
    current_status = models.CharField(max_length=100, choices=CURRENT_STATUS_CHOICES)
    discontinuation_reason = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} for {self.patient}'
