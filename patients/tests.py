from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Patient
from datetime import date

User = get_user_model()

class PatientModelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='1234567890', password='testpass')
        self.patient = Patient.objects.create(
            user=self.user,
            national_id='NID123456',
            birthdate=date(1990, 1, 1),
            gender='M',
            marital_status='single',
            ms_type='relapsing_remitting'
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.user, self.user)
        self.assertEqual(self.patient.national_id, 'NID123456')
        self.assertEqual(self.patient.gender, 'M')

class PatientProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone_number='0987654321', password='testpass')
        self.patient = Patient.objects.create(
            user=self.user,
            national_id='NID654321',
            birthdate=date(1985, 5, 15),
            gender='F',
            marital_status='married',
            ms_type='primary_progressive'
        )
        self.client = APIClient()
        self.url = reverse('patient-profile')

    def test_profile_access_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['national_id'], 'NID654321')
        self.assertEqual(response.data['gender'], 'F')

    def test_profile_access_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_not_found(self):
        new_user = User.objects.create_user(phone_number='1112223333', password='testpass')
        self.client.force_authenticate(user=new_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
