import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
from authentication.firebase_config import pyrebase_auth
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from authentication.models import FirebaseUser
from firebase_admin import auth

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

def test_authentication():
    try:
        # Test user credentials - replace with your test user
        email = "test@example.com"
        password = "testpassword123"
    except Exception as e:
        print("❌ An error occurred while setting up test credentials:", str(e))

        # Step 1: Sign in with email and password
        try:
            user = pyrebase_auth.sign_in_with_email_and_password(email, password)
            id_token = user['idToken']
            print("✅ Successfully signed in and got ID token")
        except Exception as e:
            print("❌ Failed to sign in:", str(e))
            return

        # Step 2: Test the predict endpoint
        try:
            response = requests.post(
                'http://localhost:8000/api/predict/',
                headers={
                    'Authorization': f'Bearer {id_token}',
                    'Content-Type': 'application/json'
                },
                json={
                    'location': 'test_location',
                    'sqft': 1000,
                    'bhk': 2
                }
            )
            
            print("\nAPI Response Status:", response.status_code)
            print("API Response Body:", json.dumps(response.json(), indent=2))
            
            if response.status_code == 200:
                print("✅ Successfully made authenticated API request")
            else:
                print("❌ API request failed with status code:", response.status_code)
                
        except requests.exceptions.ConnectionError:
            print("❌ Failed to connect to the API. Make sure the Django server is running.")
        except Exception as e:
            print("❌ Error making API request:", str(e))

class FirebaseAuthErrorTests(APITestCase):
    """
    Test suite for Firebase authentication error handling.
    
    Tests various error scenarios that can occur during Firebase
    authentication, ensuring proper error handling and user feedback.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/auth/signup'
        self.login_url = '/api/auth/login'
        self.refresh_url = '/api/auth/refresh'
        
        self.valid_signup_data = {
            'email': 'test@example.com',
            'password': 'Test@123',
            'name': 'Test User'
        }
        
        self.valid_login_data = {
            'email': 'test@example.com',
            'password': 'Test@123'
        }

    @patch('authentication.views.pyrebase_auth')
    def test_signup_email_already_exists(self, mock_auth):
        """Test signup with existing email"""
        mock_auth.create_user_with_email_and_password.side_effect = Exception(
            'EMAIL_EXISTS'
        )
        
        response = self.client.post(
            self.signup_url,
            self.valid_signup_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('EMAIL_EXISTS', str(response.data['error']))

    @patch('authentication.views.pyrebase_auth')
    def test_signup_weak_password(self, mock_auth):
        """Test signup with weak password"""
        data = self.valid_signup_data.copy()
        data['password'] = '123'
        
        mock_auth.create_user_with_email_and_password.side_effect = Exception(
            'WEAK_PASSWORD'
        )
        
        response = self.client.post(
            self.signup_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('WEAK_PASSWORD', str(response.data['error']))

    @patch('authentication.views.pyrebase_auth')
    def test_login_user_not_found(self, mock_auth):
        """Test login with non-existent user"""
        mock_auth.sign_in_with_email_and_password.side_effect = Exception(
            'EMAIL_NOT_FOUND'
        )
        
        response = self.client.post(
            self.login_url,
            self.valid_login_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_login_wrong_password(self, mock_auth):
        """Test login with incorrect password"""
        mock_auth.sign_in_with_email_and_password.side_effect = Exception(
            'INVALID_PASSWORD'
        )
        
        response = self.client.post(
            self.login_url,
            self.valid_login_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_invalid_email_format(self):
        """Test login with malformed email"""
        data = self.valid_login_data.copy()
        data['email'] = 'invalid-email'
        
        response = self.client.post(
            self.login_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('authentication.views.pyrebase_auth')
    def test_token_refresh_invalid_token(self, mock_auth):
        """Test token refresh with invalid refresh token"""
        mock_auth.refresh.side_effect = Exception('Invalid refresh token')
        
        response = self.client.post(
            self.refresh_url,
            {'refresh_token': 'invalid-token'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('authentication.middleware.auth')
    def test_middleware_token_verification_failure(self, mock_auth):
        """Test authentication middleware with invalid token"""
        mock_auth.verify_id_token.side_effect = auth.InvalidIdTokenError('Invalid token')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid-token')
        response = self.client.get('/api/predictions/history')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('authentication.middleware.auth')
    def test_middleware_expired_token(self, mock_auth):
        """Test authentication middleware with expired token"""
        mock_auth.verify_id_token.side_effect = auth.ExpiredIdTokenError('Token expired')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token expired-token')
        response = self.client.get('/api/predictions/history')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('authentication.middleware.auth')
    def test_middleware_revoked_token(self, mock_auth):
        """Test authentication middleware with revoked token"""
        mock_auth.verify_id_token.side_effect = auth.RevokedIdTokenError('Token revoked')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token revoked-token')
        response = self.client.get('/api/predictions/history')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_authorization_header(self):
        """Test request without authorization header"""
        response = self.client.get('/api/predictions/history')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_malformed_authorization_header(self):
        """Test request with malformed authorization header"""
        self.client.credentials(HTTP_AUTHORIZATION='Invalid-Format Token')
        response = self.client.get('/api/predictions/history')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signup_missing_required_fields(self):
        """Test signup with missing required fields"""
        required_fields = ['email', 'password', 'name']
        
        for field in required_fields:
            data = self.valid_signup_data.copy()
            del data[field]
            
            response = self.client.post(
                self.signup_url,
                data,
                format='json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)

    def tearDown(self):
        """Clean up after each test"""
        self.client.credentials()

if __name__ == "__main__":
    test_authentication()