from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from authentication.models import FirebaseUser
from predictions.models import RentPrediction
from django.urls import reverse
from unittest.mock import patch

class APIEndpointTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = FirebaseUser(uid='test_user_id', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        
        # Create some test predictions
        self.prediction = RentPrediction.objects.create(
            user_id=self.user.uid,
            location='Mumbai',
            bhk=2,
            sqft=1000.0,
            predicted_rent=25000.0
        )

    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

    def test_supported_locations(self):
        """Test getting list of supported locations"""
        response = self.client.get(reverse('supported_locations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['locations'], list)
        self.assertGreater(len(response.data['locations']), 0)

    def test_rent_trends(self):
        """Test getting rent trends data"""
        response = self.client.get(reverse('rent_trends'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('trends', response.data)

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        # Remove authentication
        self.client.force_authenticate(user=None)
        
        # Try accessing protected endpoint
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('predictions.views.model.predict')
    def test_rent_prediction_flow(self, mock_predict):
        """Test the complete rent prediction flow"""
        # Mock the model prediction
        mock_predict.return_value = [25000.0]
        
        # Make a prediction request
        prediction_data = {
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
        
        # Make prediction
        response = self.client.post(reverse('predict_rent'), prediction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_rent', response.data)
        prediction_id = response.data['id']
        
        # Verify prediction was saved
        saved_prediction = RentPrediction.objects.get(id=prediction_id)
        self.assertEqual(saved_prediction.location, prediction_data['location'])
        self.assertEqual(saved_prediction.bhk, prediction_data['bhk'])
        
        # Check prediction history
        history_response = self.client.get(reverse('prediction_history'))
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(history_response.data), 0)
        self.assertEqual(history_response.data[0]['id'], prediction_id)

    def test_invalid_prediction_request(self):
        """Test handling of invalid prediction requests"""
        invalid_data = {
            'location': 'InvalidCity',
            'sqft': -100,  # Invalid value
            'bhk': 10  # Invalid value
        }
        
        response = self.client.post(reverse('predict_rent'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_rate_limiting(self):
        """Test rate limiting on API endpoints"""
        # Make multiple requests in quick succession
        for _ in range(5):
            self.client.get(reverse('supported_locations'))
        
        # This request should be rate limited
        response = self.client.get(reverse('supported_locations'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test with malformed JSON
        response = self.client.post(
            reverse('predict_rent'),
            data='{"invalid": json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with missing required fields
        response = self.client.post(
            reverse('predict_rent'),
            {'location': 'Mumbai'},  # Missing required fields
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with invalid content type
        response = self.client.post(
            reverse('predict_rent'),
            data='plain text',
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
