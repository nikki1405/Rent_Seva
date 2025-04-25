from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import EstimateHistory, FirebaseUser

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.signup_url = '/api/auth/signup'
        self.login_url = '/api/auth/login'
        self.logout_url = '/api/auth/logout'
        self.refresh_url = '/api/auth/refresh'
        
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'Test@123',
            'name': 'Test User',
            'mobile': '1234567890'
        }
        
        self.firebase_response = {
            'idToken': 'dummy-token',
            'refreshToken': 'dummy-refresh-token',
            'email': 'test@example.com',
            'localId': 'dummy-uid'
        }

    @patch('authentication.views.pyrebase_auth')
    def test_signup_success(self, mock_auth):
        mock_auth.create_user_with_email_and_password.return_value = self.firebase_response
        
        response = self.client.post(self.signup_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_signup_invalid_email(self, mock_auth):
        mock_auth.create_user_with_email_and_password.side_effect = Exception('Invalid email')
        
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'invalid-email'
        
        response = self.client.post(self.signup_url, invalid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_login_success(self, mock_auth):
        mock_auth.sign_in_with_email_and_password.return_value = self.firebase_response
        
        response = self.client.post(self.login_url, {
            'email': self.valid_payload['email'],
            'password': self.valid_payload['password']
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_login_invalid_credentials(self, mock_auth):
        mock_auth.sign_in_with_email_and_password.side_effect = Exception('Invalid credentials')
        
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_logout_success(self):
        # Set up authenticated session
        self.client.credentials(HTTP_AUTHORIZATION='Token dummy-token')
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_token_refresh(self, mock_auth):
        mock_auth.refresh.return_value = {'idToken': 'new-dummy-token'}
        
        response = self.client.post(self.refresh_url, {
            'refresh_token': 'dummy-refresh-token'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class FirebaseUserTests(TestCase):
    def test_firebase_user_creation(self):
        user = FirebaseUser(uid='test-uid', email='test@example.com')
        
        self.assertEqual(user.uid, 'test-uid')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.id, 'test-uid')

class EstimateHistoryTests(TestCase):
    def test_estimate_history_creation(self):
        history = EstimateHistory.objects.create(
            user_id='test-uid',
            location='Mumbai',
            bhk=2,
            sqft=1000.0,
            predicted_rent=25000.0
        )
        
        self.assertEqual(history.user_id, 'test-uid')
        self.assertEqual(history.location, 'Mumbai')
        self.assertEqual(history.bhk, 2)
        self.assertEqual(history.sqft, 1000.0)
        self.assertEqual(history.predicted_rent, 25000.0)
        self.assertIsNotNone(history.created_at)

    def test_estimate_history_ordering(self):
        EstimateHistory.objects.create(
            user_id='test-uid',
            location='Mumbai',
            bhk=2,
            sqft=1000.0,
            predicted_rent=25000.0
        )
        EstimateHistory.objects.create(
            user_id='test-uid',
            location='Delhi',
            bhk=3,
            sqft=1500.0,
            predicted_rent=35000.0
        )
        
        histories = EstimateHistory.objects.all()
        self.assertEqual(histories[0].location, 'Delhi')  # Most recent first
