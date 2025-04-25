TEST_CONFIG = {
    'api_url': "http://localhost:8000/api/predict/",
    'min_rent_per_bhk': 5000,
    'area_scale_factor': 0.8,
    'timeout': 10,  # seconds
    'retries': 3
}

import requests
import json
import numpy as np

def validate_prediction(predicted_rent, test_case):
    """Validate if the prediction seems reasonable"""
    area = test_case['built_area_sqft']
    bhk = test_case['bhk']
    location = test_case['location']
    
    # Define Vizag-specific areas and their tiers
    vizag_premium = ["MVP Colony", "Beach Road", "Seethammadhara", "Lawsons Bay Colony"]
    vizag_mid = ["Madhurawada", "Rushikonda", "Gajuwaka", "Pendurthi"]
    vizag_budget = ["Gopalapatnam", "NAD Junction", "Aganampudi", "Chintalagraharam"]
    
    # Adjust base rates by area
    base_rates = {
        "premium": {"min": 12, "max": 25},  # Premium Vizag areas
        "mid": {"min": 8, "max": 20},      # Mid-range Vizag areas
        "budget": {"min": 6, "max": 15}     # Budget Vizag areas
    }
    
    # Get appropriate area rates
    if location in vizag_premium:
        rates = base_rates["premium"]
    elif location in vizag_mid:
        rates = base_rates["mid"]
    else:
        rates = base_rates["budget"]
    
    # Calculate reasonable rent thresholds
    min_rent_per_sqft = rates["min"]
    max_rent_per_sqft = rates["max"]
    
    # Adjust minimum rent per BHK based on area
    if location in vizag_premium:
        min_rent_per_bhk = 15000
    elif location in vizag_mid:
        min_rent_per_bhk = 12000
    else:
        min_rent_per_bhk = 8000

    # Calculate actual rent per square foot
    rent_per_sqft = predicted_rent / area if predicted_rent > 0 else 0
    
    # Add maximum rent cap based on location
    max_total_rent = {
        "MVP Colony": 100000,
        "Madhurawada": 80000,
        "Beach Road": 120000,
        "Seethammadhara": 90000,
        "Lawsons Bay Colony": 100000,
        "Rushikonda": 85000,
        "Gajuwaka": 70000,
        "Pendurthi": 65000,
        "Vizag": 100000  # General Vizag area
    }.get(location, 60000)  # Default max rent for other locations

    # Enhanced validation checks with more flexible thresholds
    checks = {
        f"Rent per sqft in range for {location}": 
            (min_rent_per_sqft * 0.8) <= rent_per_sqft <= (max_rent_per_sqft * 1.2),
        "Rent scales with area": 
            predicted_rent >= (area * min_rent_per_sqft * 0.7),
        "Rent scales with BHK": 
            predicted_rent >= (bhk * min_rent_per_bhk * 0.8),
        "Below maximum rent cap":
            predicted_rent <= (max_total_rent * 1.1),
        "Above minimum viable rent":
            predicted_rent >= (min_rent_per_bhk * bhk * 0.7)
    }
    
    # Add debug information
    print(f"\nDebug Info for {location}:")
    print(f"Min rent/sqft: ₹{min_rent_per_sqft}")
    print(f"Max rent/sqft: ₹{max_rent_per_sqft}")
    print(f"Actual rent/sqft: ₹{rent_per_sqft:.2f}")
    print(f"Min rent/BHK: ₹{min_rent_per_bhk}")
    print(f"Max total rent: ₹{max_total_rent}")
    
    return checks

def test_prediction(test_case):
    url = "http://localhost:8000/api/predict/"
    
    try:
        response = requests.post(url, json=test_case)
        predicted_rent = response.json()['predicted_rent']
        
        print(f"\nTest Case:")
        print(f"Location: {test_case['location']}")
        print(f"Area: {test_case['built_area_sqft']} sq ft")
        print(f"BHK: {test_case['bhk']}")
        print(f"Status Code: {response.status_code}")
        print(f"Predicted Rent: ₹{predicted_rent:,.2f}")
        print(f"Rent per sq ft: ₹{predicted_rent/test_case['built_area_sqft']:.2f}")
        
        validation_results = validate_prediction(predicted_rent, test_case)
        print("\nValidation Results:")
        for check, result in validation_results.items():
            print(f"{check}: {'✓' if result else '✗'}")
        
        return {
            'success': all(validation_results.values()),
            'predicted_rent': predicted_rent,
            'rent_per_sqft': predicted_rent / test_case['built_area_sqft']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {
            'success': False,
            'predicted_rent': 0,
            'rent_per_sqft': 0
        }

def print_test_statistics(test_results):
    total_tests = len(test_results)
    successful = sum(1 for result in test_results if result['success'])
    
    print("\n=== Test Statistics ===")
    print(f"Total Tests Run: {total_tests}")
    print(f"Successful: {successful}")
    print(f"Failed: {total_tests - successful}")
    print(f"Success Rate: {(successful/total_tests)*100:.1f}%")
    
    print("\nDetailed Results by Location:")
    for result in test_results:
        location = result['location']
        status = "✓" if result['success'] else "✗"
        predicted = result['predicted_rent']
        per_sqft = result['rent_per_sqft']
        print(f"{location}: {status} (₹{predicted:,.2f} | ₹{per_sqft:.2f}/sqft)")
    
    print("\nRent Range Analysis:")
    for result in test_results:
        location = result['location']
        rent = result['predicted_rent']
        area = test_cases[test_results.index(result)]['built_area_sqft']
        bhk = test_cases[test_results.index(result)]['bhk']
        print(f"{location} ({bhk}BHK, {area}sqft): ₹{rent:,.2f} "
              f"(₹{result['rent_per_sqft']:.2f}/sqft)")

if __name__ == "__main__":
    test_cases = [
        {
            "location": "Madhurawada",
            "built_area_sqft": 850,
            "bhk": 2,
            "bathrooms": 2,
            "lift": True,
            "air_conditioner": False,
            "parking": True,
            "gym": False,
            "security": True,
            "water_supply": True
        },
        {
            "location": "MVP Colony",
            "built_area_sqft": 1000,
            "bhk": 2,
            "bathrooms": 2,
            "lift": True,
            "air_conditioner": True,
            "parking": True,
            "gym": False,
            "security": True,
            "water_supply": True
        },
        {
            "location": "Pendurthi",
            "built_area_sqft": 1200,
            "bhk": 3,
            "bathrooms": 2,
            "lift": True,
            "air_conditioner": True,
            "parking": True,
            "gym": True,
            "security": True,
            "water_supply": True
        }
    ]

    test_results = []
    for case in test_cases:
        result = test_prediction(case)
        test_results.append({
            'location': case['location'],
            'success': result['success'],
            'predicted_rent': result['predicted_rent'],
            'rent_per_sqft': result['rent_per_sqft']
        })
    
    print_test_statistics(test_results)

import os
import sys
import django
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.rentpred.settings')
django.setup()

# Now we can import from Django apps
from backend.authentication.models import FirebaseUser, EstimateHistory

class APIEndpointTests(APITestCase):
    """
    Test suite for API endpoints.
    
    Tests all API endpoints for correct functionality, proper error handling,
    and response format validation.
    """
    
    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()
        self.user = FirebaseUser(uid='test_user_id', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

    def test_supported_locations(self):
        """Test supported locations endpoint"""
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['locations'], list)
        self.assertGreater(len(response.data['locations']), 0)

    @patch('authentication.views.pyrebase_auth')
    def test_user_profile(self, mock_auth):
        """Test user profile endpoints"""
        # Mock Firebase response
        mock_auth.get_account_info.return_value = {
            'users': [{
                'localId': 'test_user_id',
                'email': 'test@example.com',
                'emailVerified': True
            }]
        }
        
        # Get profile
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        
        # Update profile
        update_data = {'name': 'Updated Name'}
        response = self.client.patch(
            '/api/auth/profile/',
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_api_versioning(self):
        """Test API version headers"""
        response = self.client.get(
            '/api/health/',
            HTTP_ACCEPT='application/json; version=1.0'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('API-Version', response['X-API-Version'])

    def test_api_documentation(self):
        """Test API documentation endpoints"""
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('application/json', response['Content-Type'])

    def test_cors_headers(self):
        """Test CORS headers"""
        response = self.client.options(
            '/api/health/',
            HTTP_ORIGIN='http://localhost:3000'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Access-Control-Allow-Origin', response)
        self.assertIn('Access-Control-Allow-Methods', response)
        self.assertIn('Access-Control-Allow-Headers', response)

    def test_prediction_endpoints(self):
        """Test prediction-related endpoints"""
        # Test locations list
        response = self.client.get('/api/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test rent trends
        response = self.client.get('/api/trends/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('trends', response.data)
        
        # Test prediction with missing data
        response = self.client.post('/api/predict/rent/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test prediction history
        response = self.client.get('/api/predictions/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_error_handling(self):
        """Test API error handling"""
        # Test 404
        response = self.client.get('/api/nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Test method not allowed
        response = self.client.delete('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test invalid JSON
        response = self.client.post(
            '/api/predict/rent/',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authentication_required(self):
        """Test authentication requirements"""
        # Remove authentication
        self.client.force_authenticate(user=None)
        
        protected_endpoints = [
            '/api/predictions/history/',
            '/api/predict/rent/',
            '/api/auth/profile/'
        ]
        
        for endpoint in protected_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should require authentication"
            )

    def test_response_format(self):
        """Test API response format consistency"""
        endpoints = [
            '/api/health/',
            '/api/locations/',
            '/api/trends/'
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response.data, dict)
            self.assertTrue(all(isinstance(k, str) for k in response.data.keys()))

    def test_pagination(self):
        """Test API pagination"""
        # Create test predictions
        prediction_data = {
            'location': 'Mumbai',
            'sqft': 1000.0,
            'bhk': 2
        }
        
        # Create multiple predictions
        for _ in range(25):  # More than default page size
            self.client.post(
                '/api/predict/rent/',
                prediction_data,
                format='json'
            )
        
        # Test pagination
        response = self.client.get('/api/predictions/history/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
        
        # Test invalid page
        response = self.client.get('/api/predictions/history/?page=999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_filtering(self):
        """Test API filtering capabilities"""
        # Test location filter
        response = self.client.get('/api/predictions/history/?location=Mumbai')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test date range filter
        response = self.client.get(
            '/api/predictions/history/?start_date=2024-01-01&end_date=2024-12-31'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test BHK filter
        response = self.client.get('/api/predictions/history/?bhk=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        """Clean up after tests"""
        self.client.credentials()