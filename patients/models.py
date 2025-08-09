from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.validations import validate_iranian_national_id, validate_name, validate_address, validate_iranian_phone_number


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patient_last_modified_by')

    # Personal Information
    national_id = models.CharField(max_length=50, unique=True, validators=[validate_iranian_national_id])
    birthdate= models.DateField()

    GENDER_CHOICES = (
        ('M', "Male"),
        ('F', "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    MARITAL_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed')
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES)
    education_level = models.CharField(max_length=100, validators=[validate_name])
    address = models.CharField(max_length=200, validators=[validate_address])
    emergency_contact_name = models.CharField(max_length=100, validators=[validate_name])
    emergency_contact_phone = models.CharField(max_length=15, validators=[validate_iranian_phone_number])
    emergency_contact_relationship = models.CharField(max_length=100, validators=[validate_name])
    years_employed = models.PositiveIntegerField()
    current_occupation= models.CharField(max_length=100, validators=[validate_name], blank=True, default='')

    # Medical History
    MS_TYPE_CHOICES = (
        ('RRMS', 'Relapsing Remitting'),
        ('PPMS', 'Primary Progressive'),
        ('SPMS', 'Secondary Progressive'),
        ('CIS', 'Clinically Isolated Syndrome'),
    )
    ms_type = models.CharField(max_length=4, choices=MS_TYPE_CHOICES)
    ms_diagnosis_date= models.DateField()
    # number_of_relapses
    family_medical_history = models.TextField(blank=True, default='')
    caregiver_diseases = models.TextField(blank=True, default='')
    drug_allergies = models.TextField(blank=True, default='')
    food_allergies = models.TextField(blank=True, default='')

    # Treatment and Rehabilitation History
    physiotherapy_received = models.TextField(blank=True, default='')
    occupational_therapy_received = models.TextField(blank=True, default='')
    mobility_aids_used = models.TextField(blank=True, default='')
    therapist_cooperation_level = models.TextField(blank=True, default='')

    # Functional Assessments
    motor_status = models.TextField(blank=True, default='')
    muscle_strength = models.TextField(blank=True, default='')
    balance = models.TextField(blank=True, default='')
    walking_ability = models.TextField(blank=True, default='')
    adl_activities = models.TextField(blank=True, default='')
    cognitive_status = models.TextField(blank=True, default='')
    speech_status = models.TextField(blank=True, default='')
    swallowing_status = models.TextField(blank=True, default='')
    fatigue_level = models.TextField(blank=True, default='')
    psychological_status = models.TextField(blank=True, default='')

    # Environmental Evaluation
    living_environment = models.TextField(blank=True, default='')
    equipment_used_daily = models.TextField(blank=True, default='')
    equipment_used_work = models.TextField(blank=True, default='')
    environmental_modifications_needed = models.TextField(blank=True, default='')
    assistive_devices_needed = models.TextField(blank=True, default='')

    # Treatment Goals
    short_term_goals  = models.TextField(blank=True, default='')
    long_term_goals  = models.TextField(blank=True, default='')
    patient_personal_goals  = models.TextField(blank=True, default='')
    therapist_team_goals  = models.TextField(blank=True, default='')
    goal_timeline = models.TextField(blank=True, default='')

    # Occupational Therapy Treatment Plan
    recommended_exercises = models.TextField(blank=True, default='')
    fatigue_management_techniques = models.TextField(blank=True, default='')
    environmental_adaptation = models.TextField(blank=True, default='')
    family_education = models.TextField(blank=True, default='')
    caregiver_education = models.TextField(blank=True, default='')
    session_scheduling = models.TextField(blank=True, default='')
    progress_monitoring = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user}"

class PatientProgressMonitoring(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)
    performance_improvement = models.TextField(blank=True, default='')
    performance_loss = models.TextField(blank=True, default='')
    assessment_date = models.DateField()
    next_assessment_date = models.DateField()

    def __str__(self):
        return f"Patient: {self.patient} on {self.assessment_date}"


class PatientRelapse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)
    date = models.DateField()
    areas = models.TextField()

    def __str__(self):
        return f"Patient: {self.patient} on {self.date}"


class PatientMedicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, validators=[validate_name])
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} for {self.patient}"
