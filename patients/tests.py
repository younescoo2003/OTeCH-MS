from django.contrib.auth import get_user_model
from django.core.cache import caches
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient, PatientProgressMonitoring, PatientMedicine
from .serializers import PatientSerializer, PatientRegisterSerializer
import uuid

User = get_user_model()
auth_cache = caches['auth']

class PatientProfileTests(APITestCase):
    """Tests for patient profile retrieval endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09123456789',
            first_name='John',
            last_name='Doe',
            password='testpass123',
            role='patient'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            national_id='1234567890',
            birthdate='1990-01-01',
            gender='M',
            marital_status='single',
            ms_type='RRMS'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_retrieve_profile_authenticated(self):
        """Test authenticated user can retrieve their profile"""
        response = self.client.get('/api/patient/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['phone_number'], '09123456789')
        self.assertEqual(response.data['national_id'], '1234567890')

    def test_unauthenticated_access(self):
        """Test profile endpoint requires authentication"""
        client = APIClient()
        response = client.get('/api/patient/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PatientRegistrationTests(APITestCase):
    """Tests for patient registration endpoint"""
    
    def setUp(self):
        self.valid_token = str(uuid.uuid4())
        auth_cache.set(f'verified_09123456789', self.valid_token, timeout=300)
        
        self.valid_payload = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'securepass123',
            'temp_token': self.valid_token,
            'phone_number': '09123456789',
            'national_id': '0987654321',
            'birthdate': '1995-05-15',
            'gender': 'F',
            'marital_status': 'M',
            'ms_type': 'PPMS',
            'education_level': 'BACHELORS',
            'address': '123 Main St',
            'emergency_contact_name': 'John Doe',
            'emergency_contact_phone': '09198765432',
            'emergency_contact_relationship': 'Parent'
        }

    def test_patient_registration_success(self):
        """Test successful patient registration with valid data"""
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'securepass123',
            'temp_token': self.valid_token,
            'phone_number': '09123456789',
            'national_id': '0987654321',
            'birthdate': '1995-05-15',
            'gender': 'F',
            'marital_status': 'M',
            'ms_type': 'PPMS',
            'education_level': 'BACHELORS',
            'address': '123 Main St',
            'emergency_contact_name': 'John Doe',
            'emergency_contact_phone': '09198765432',
            'emergency_contact_relationship': 'Parent'
        }
        response = self.client.post('/api/patient/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('access', response.data)

    def test_registration_invalid_temp_token(self):
        """Test registration fails with invalid temporary token"""
        data = {**self.valid_payload, 'temp_token': 'invalid-token'}
        response = self.client.post('/api/patient/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid temp token', str(response.content))

    def test_national_id_uniqueness(self):
        """Test national ID uniqueness constraint enforcement"""
        # Create existing patient with same national ID
        User.objects.create_user(
            phone_number='09111111111',
            password='testpass123',
            role='patient'
        )
        Patient.objects.create(
            user=User.objects.last(),
            national_id='1234567890',
            birthdate='1990-01-01',
            gender='M'
        )
        
        data = {**self.valid_payload, 'national_id': '1234567890'}
        response = self.client.post('/api/patient/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('national_id', response.data['errors'])

class ProgressMonitoringTests(APITestCase):
    """Tests for progress monitoring CRUD operations"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password='testpass123',
            role='patient'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            national_id='1234567890',
            birthdate='1990-01-01',
            gender='M',
            marital_status='single',
            ms_type='RRMS'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_progress_entry(self):
        """Test creating new progress monitoring entry"""
        data = {
            'date': '2025-07-13',
            'mobility_score': 75,
            'cognitive_score': 80,
            'notes': 'Steady progress'
        }
        response = self.client.post('/api/progress-monitoring/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientProgressMonitoring.objects.count(), 1)
        self.assertEqual(PatientProgressMonitoring.objects.last().patient, self.patient)

class PatientMedicineTests(APITestCase):
    """Tests for patient medicine management endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09123456789',
            password='testpass123',
            role='patient'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            national_id='1234567890',
            birthdate='1990-01-01',
            gender='M',
            marital_status='single',
            ms_type='RRMS'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.medicine = PatientMedicine.objects.create(
            patient=self.patient,
            name='Interferon beta-1a',
            dosage_amount=30,
            dosage_unit='mcg',
            frequency_per_day=7,
            frequency_description='Weekly',
            start_date='2025-01-01',
            end_date='2025-12-31'
        )

    def test_create_medicine(self):
        """Test creating a new medicine record with valid data"""
        data = {
            'name': 'Fingolimod',
            'dosage_amount': 0.5,
            'dosage_unit': 'mg',
            'frequency_per_day': 1,
            'frequency_description': 'Daily',
            'start_date': '2025-07-01'
        }
        response = self.client.post('/api/patient-medicines/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientMedicine.objects.count(), 2)
        self.assertEqual(PatientMedicine.objects.last().patient, self.patient)

    def test_list_medicines(self):
        """Test retrieving list of medicines for authenticated patient"""
        response = self.client.get('/api/patient-medicines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Interferon beta-1a')

    def test_retrieve_medicine(self):
        """Test getting single medicine record by ID"""
        url = f'/api/patient-medicines/{self.medicine.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dosage'], '30mcg')

    def test_update_medicine(self):
        """Test partial update of existing medicine record"""
        url = f'/api/patient-medicines/{self.medicine.id}/'
        data = {'dosage_amount': 40, 'dosage_unit': 'mcg', 'frequency_per_day': 14, 'frequency_description': 'Bi-weekly'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.dosage, '40mcg')

    def test_delete_medicine(self):
        """Test deletion of existing medicine record"""
        url = f'/api/patient-medicines/{self.medicine.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PatientMedicine.objects.count(), 0)

    def test_medicine_validation(self):
        """Test validation of medicine model constraints"""
        data = {
            'name': 'A' * 101,  # Exceeds max length
            'dosage': '',
            'start_date': 'invalid-date'
        }
        response = self.client.post('/api/patient-medicines/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('dosage', response.data)
        self.assertIn('start_date', response.data)

    def test_unauthorized_medicine_access(self):
        """Test user cannot access another patient's medicines"""
        other_user = User.objects.create_user(
            phone_number='09111111111',
            password='testpass123',
            role='patient'
        )
        other_client = APIClient()
        refresh = RefreshToken.for_user(other_user)
        other_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Try to access another user's medicine
        url = f'/api/patient-medicines/{self.medicine.id}/'
        response = other_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination(self):
        """Test medicine list pagination configuration"""
        # Create 15 test medicines
        for i in range(1, 16):
            PatientMedicine.objects.create(
                patient=self.patient,
                name=f'Medicine {i}',
                dosage_amount=i,
                dosage_unit='mg',
                frequency_per_day=1,
                frequency_description='Daily',
                start_date='2025-01-01'
            )
            
        response = self.client.get('/api/patient-medicines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 16)  # 15 new + 1 existing
        self.assertEqual(len(response.data['results']), 10)  # Default page size