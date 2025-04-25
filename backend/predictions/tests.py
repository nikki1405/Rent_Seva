from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
import time
from .models import RentPrediction
from authentication.models import FirebaseUser

class RentPredictionTests(APITestCase):
    def setUp(self):
        # Setup test user
        self.user = FirebaseUser(uid='test_user_id', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        
        # Create sample prediction
        self.prediction = RentPrediction.objects.create(
            user_id=self.user.uid,
            location='Mumbai',
            bhk=2,
            sqft=1000.0,
            predicted_rent=25000.0
        )

    def test_predict_rent(self):
        """Test rent prediction endpoint"""
        url = reverse('predict_rent')
        data = {
            'location': 'Mumbai',
            'sqft': 1000.0,
            'bhk': 2,
            'lift': 1,
            'air_conditioner': 1,
            'parking': 1,
            'gym': 0,
            'security': 1,
            'water_supply': 1
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_rent', response.data)
        self.assertIn('timestamp', response.data)

    def test_get_prediction_history(self):
        """Test prediction history endpoint"""
        url = reverse('prediction_history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['location'], 'Mumbai')

    def test_predict_rent_missing_fields(self):
        """Test prediction with missing required fields"""
        url = reverse('predict_rent')
        data = {
            'location': 'Mumbai',
            'sqft': 1000.0
            # Missing bhk field
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_predict_rent_invalid_values(self):
        """Test prediction with invalid values"""
        url = reverse('predict_rent')
        data = {
            'location': 'Mumbai',
            'sqft': -1000.0,  # Invalid negative value
            'bhk': 2
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RentPredictionModelTests(TestCase):
    def test_rent_prediction_creation(self):
        """Test RentPrediction model creation and string representation"""
        prediction = RentPrediction.objects.create(
            user_id='test_user',
            location='Delhi',
            bhk=3,
            sqft=1500.0,
            predicted_rent=35000.0
        )
        
        self.assertEqual(str(prediction), 'Delhi - 3BHK - ₹35,000.00')
        self.assertEqual(prediction.location, 'Delhi')
        self.assertEqual(prediction.bhk, 3)

class RateLimitTests(APITestCase):
    """
    Test suite for API rate limiting functionality.
    
    Tests both burst and sustained rate limiting for predictions
    and history endpoints.
    """
    
    def setUp(self):
        """Set up test case with authenticated user"""
        self.client = APIClient()
        self.user = FirebaseUser(uid='test_user_id', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        
        self.valid_prediction_data = {
            'location': 'Mumbai',
            'sqft': 1000.0,
            'bhk': 2,
            'lift': 1,
            'parking': 1,
            'security': 1
        }

    @patch('predictions.views.model.predict')
    def test_burst_rate_limit(self, mock_predict):
        """Test burst rate limiting for predictions"""
        mock_predict.return_value = [25000.0]
        
        # Make requests up to the burst limit
        for i in range(5):  # Burst limit is 5/minute
            response = self.client.post(
                reverse('predict_rent'),
                self.valid_prediction_data,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Next request should be throttled
        response = self.client.post(
            reverse('predict_rent'),
            self.valid_prediction_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    @patch('predictions.views.model.predict')
    def test_sustained_rate_limit(self, mock_predict):
        """Test sustained (daily) rate limiting"""
        mock_predict.return_value = [25000.0]
        
        # Create 20 predictions (daily limit)
        for i in range(20):
            response = self.client.post(
                reverse('predict_rent'),
                self.valid_prediction_data,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            time.sleep(0.1)  # Small delay to avoid burst limit
        
        # 21st request should be throttled
        response = self.client.post(
            reverse('predict_rent'),
            self.valid_prediction_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_history_rate_limit(self):
        """Test rate limiting for prediction history endpoint"""
        # Make multiple requests to history endpoint
        for i in range(5):  # Burst limit
            response = self.client.get(reverse('prediction_history'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Next request should be throttled
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_unauthenticated_rate_limit(self):
        """Test stricter rate limiting for unauthenticated requests"""
        self.client.force_authenticate(user=None)
        
        # Make requests up to anonymous limit
        for i in range(3):  # Anonymous limit is 3/hour
            response = self.client.get(reverse('supported_locations'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Next request should be throttled
        response = self.client.get(reverse('supported_locations'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_rate_limit_headers(self):
        """Test presence of rate limit headers in response"""
        response = self.client.post(
            reverse('predict_rent'),
            self.valid_prediction_data,
            format='json'
        )
        
        self.assertTrue('X-RateLimit-Limit' in response.headers)
        self.assertTrue('X-RateLimit-Remaining' in response.headers)
        self.assertTrue('X-RateLimit-Reset' in response.headers)

    def tearDown(self):
        """Clean up after each test"""
        RentPrediction.objects.all().delete()
