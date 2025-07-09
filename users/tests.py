from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Assuming URL names
        self.login_url = reverse('login')
        self.send_otp_url = reverse('send-otp')
        self.verify_otp_url = reverse('verify-otp')

        self.user_data = {
            'phone_number': '+1234567890',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }

    def test_register_view_success(self):
        response = self.client.post(self.register_url, data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['phone_number'], self.user_data['phone_number'])
        self.assertEqual(response.data['user']['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['user']['last_name'], self.user_data['last_name'])

    def test_register_view_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data.pop('phone_number')
        response = self.client.post(self.register_url, data=invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_login_view_success(self):
        # First register the user
        User.objects.create_user(**self.user_data)
        login_data = {
            'phone_number': self.user_data['phone_number'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['phone_number'], self.user_data['phone_number'])

    def test_login_view_invalid_data(self):
        login_data = {
            'phone_number': self.user_data['phone_number'],
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    @patch('users.serializers.SendOTPSerializer.save')
    def test_send_otp_view_success(self, mock_save):
        mock_save.return_value.temp_token = 'temp123token'
        send_otp_data = {'phone_number': self.user_data['phone_number']}
        response = self.client.post(self.send_otp_url, data=send_otp_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('temp_token', response.data)
        self.assertEqual(response.data['message'], 'OTP sent successfully')
        self.assertEqual(response.data['temp_token'], 'temp123token')

    def test_send_otp_view_invalid_data(self):
        send_otp_data = {}  # Missing phone_number
        response = self.client.post(self.send_otp_url, data=send_otp_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    @patch('users.serializers.VerifyOTPSerializer.save')
    def test_verify_otp_view_success(self, mock_save):
        mock_save.return_value = User(**self.user_data)
        verify_otp_data = {
            'phone_number': self.user_data['phone_number'],
            'otp': '123456',
            'temp_token': 'temp123token'
        }
        response = self.client.post(self.verify_otp_url, data=verify_otp_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'go register')

    def test_verify_otp_view_invalid_data(self):
        verify_otp_data = {
            'phone_number': self.user_data['phone_number'],
            'otp': 'wrongotp',
            'temp_token': 'temp123token'
        }
        response = self.client.post(self.verify_otp_url, data=verify_otp_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
