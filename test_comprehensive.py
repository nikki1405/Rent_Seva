import requests
import json
import pandas as pd
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
import numpy as np
import os

def validate_vizag_rent(result):
    """Validate if the predicted rent is reasonable for Vizag"""
    location = result['location']
    bhk = result['bhk']
    area = result['area']
    rent = result['predicted_rent']
    
    # Define realistic rent ranges for Vizag areas
    rent_ranges = {
        "MVP Colony": {
            1: {"min": 8000, "max": 12000},
            2: {"min": 12000, "max": 18000},
            3: {"min": 16000, "max": 25000}
        },
        "Madhurawada": {
            1: {"min": 6000, "max": 10000},
            2: {"min": 10000, "max": 15000},
            3: {"min": 14000, "max": 20000}
        },
        "Gopalapatnam": {
            1: {"min": 5000, "max": 8000},
            2: {"min": 8000, "max": 12000},
            3: {"min": 12000, "max": 16000}
        }
    }
    
    if location in rent_ranges:
        range_for_bhk = rent_ranges[location].get(bhk, {})
        min_rent = range_for_bhk.get("min", 0)
        max_rent = range_for_bhk.get("max", float('inf'))
        
        is_valid = min_rent <= rent <= max_rent
        return {
            'is_valid': is_valid,
            'expected_range': f"₹{min_rent:,} - ₹{max_rent:,}",
            'difference': rent - ((min_rent + max_rent) / 2)
        }
    return None

def test_prediction(test_case):
    """Test a single prediction"""
    url = "http://localhost:8000/api/predict/"
    
    try:
        response = requests.post(url, json=test_case)
        predicted_rent = response.json()['predicted_rent']
        
        # Calculate rent per sqft
        rent_per_sqft = predicted_rent / test_case['built_area_sqft']
        
        return {
            'location': test_case['location'],
            'bhk': test_case['bhk'],
            'area': test_case['built_area_sqft'],
            'predicted_rent': predicted_rent,
            'rent_per_sqft': rent_per_sqft
        }
    except Exception as e:
        print(f"Error testing {test_case['location']}: {str(e)}")
        return None

# Updated test cases with more realistic configurations
test_cases = [
    # MVP Colony - Premium Area
    {
        "location": "MVP Colony",
        "built_area_sqft": 650,  # Reduced area
        "bhk": 1,  # Testing 1BHK
        "bathrooms": 1,
        "lift": True,
        "air_conditioner": True,
        "parking": True,
        "gym": False,
        "security": True,
        "water_supply": True
    },
    {
        "location": "MVP Colony",
        "built_area_sqft": 850,
        "bhk": 2,
        "bathrooms": 2,
        "lift": True,
        "air_conditioner": True,
        "parking": True,
        "gym": False,
        "security": True,
        "water_supply": True
    },
    # Madhurawada - Mid Range
    {
        "location": "Madhurawada",
        "built_area_sqft": 600,
        "bhk": 1,
        "bathrooms": 1,
        "lift": False,  # More realistic for the area
        "air_conditioner": False,
        "parking": True,
        "gym": False,
        "security": True,
        "water_supply": True
    },
    {
        "location": "Madhurawada",
        "built_area_sqft": 800,
        "bhk": 2,
        "bathrooms": 2,
        "lift": True,
        "air_conditioner": False,
        "parking": True,
        "gym": False,
        "security": True,
        "water_supply": True
    }
]

if __name__ == "__main__":
    print("Starting Vizag-specific Rent Testing...")
    results = []
    
    for case in test_cases:
        result = test_prediction(case)
        if result:
            # Validate Vizag rents
            validation = validate_vizag_rent(result)
            if validation:
                result['validation'] = validation
            results.append(result)
    
    print("\n=== Test Results Summary ===")
    print(f"Total test cases: {len(test_cases)}")
    print(f"Successful predictions: {len(results)}")
    
    print("\n=== Detailed Results ===")
    for result in results:
        print(f"\nLocation: {result['location']}")
        print(f"Configuration: {result['bhk']}BHK, {result['area']} sq ft")
        print(f"Predicted Rent: ₹{result['predicted_rent']:,.2f}")
        print(f"Rate per sq ft: ₹{result['rent_per_sqft']:.2f}")
        
        if 'validation' in result:
            validation = result['validation']
            status = "✓" if validation['is_valid'] else "✗"
            print(f"Validation: {status}")
            print(f"Expected Range: {validation['expected_range']}")
            print(f"Difference from mean: ₹{validation['difference']:,.2f}")
    
    # Save results with validation
    df_results = pd.DataFrame(results)
    df_results.to_csv('vizag_rent_test_results.csv', index=False)
    print("\nTest results saved to 'vizag_rent_test_results.csv'")

class ComprehensiveIntegrationTests(APITestCase):
    """
    Integration test suite for the complete rent prediction system.
    
    Tests the entire flow from authentication through prediction,
    ensuring all components work together correctly.
    """
    
    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()
        
        # Authentication endpoints
        self.signup_url = '/api/auth/signup'
        self.login_url = '/api/auth/login'
        self.predict_url = '/api/predict/rent'
        self.history_url = '/api/predictions/history'
        
        # Test user credentials
        self.test_user = {
            'email': 'integration@test.com',
            'password': 'Integration@123',
            'name': 'Integration Test User'
        }
        
        # Test prediction data
        self.prediction_data = {
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

    @patch('authentication.views.pyrebase_auth')
    @patch('predictions.views.model.predict')
    def test_complete_user_flow(self, mock_predict, mock_auth):
        """Test complete user flow from signup through prediction"""
        
        # Mock Firebase responses
        mock_auth.create_user_with_email_and_password.return_value = {
            'idToken': 'test-token',
            'refreshToken': 'test-refresh-token',
            'localId': 'test-uid'
        }
        
        mock_auth.sign_in_with_email_and_password.return_value = {
            'idToken': 'test-token',
            'refreshToken': 'test-refresh-token',
            'localId': 'test-uid'
        }
        
        # Mock prediction
        mock_predict.return_value = np.array([25000.0])
        
        # Step 1: Sign up
        signup_response = self.client.post(
            self.signup_url,
            self.test_user,
            format='json'
        )
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', signup_response.data)
        
        # Extract token and set auth header
        token = signup_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # Step 2: Make prediction
        predict_response = self.client.post(
            self.predict_url,
            self.prediction_data,
            format='json'
        )
        self.assertEqual(predict_response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_rent', predict_response.data)
        
        # Step 3: Check prediction history
        history_response = self.client.get(self.history_url)
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(history_response.data), 0)
        self.assertEqual(
            history_response.data[0]['location'],
            self.prediction_data['location']
        )

    @patch('predictions.views.model.predict')
    def test_prediction_data_validation(self, mock_predict):
        """Test prediction with various input data scenarios"""
        
        # Authenticate first
        self.client.credentials(HTTP_AUTHORIZATION='Token test-token')
        mock_predict.return_value = np.array([25000.0])
        
        # Test valid ranges
        test_cases = [
            # Valid cases
            ({'sqft': 1000, 'bhk': 2}, status.HTTP_200_OK),
            ({'sqft': 500, 'bhk': 1}, status.HTTP_200_OK),
            ({'sqft': 2000, 'bhk': 3}, status.HTTP_200_OK),
            
            # Invalid cases
            ({'sqft': 50, 'bhk': 2}, status.HTTP_400_BAD_REQUEST),  # Too small
            ({'sqft': 15000, 'bhk': 2}, status.HTTP_400_BAD_REQUEST),  # Too large
            ({'sqft': 1000, 'bhk': 0}, status.HTTP_400_BAD_REQUEST),  # Invalid BHK
            ({'sqft': 1000, 'bhk': 8}, status.HTTP_400_BAD_REQUEST),  # Invalid BHK
        ]
        
        for data_mod, expected_status in test_cases:
            test_data = self.prediction_data.copy()
            test_data.update(data_mod)
            
            response = self.client.post(
                self.predict_url,
                test_data,
                format='json'
            )
            self.assertEqual(
                response.status_code,
                expected_status,
                f"Failed for data: {data_mod}"
            )

    def test_model_accuracy(self):
        """Test model prediction accuracy with test data"""
        
        # Load test data
        test_data_path = 'prediction_test_results.csv'
        if not os.path.exists(test_data_path):
            self.skipTest("Test data file not found")
            
        test_data = pd.read_csv(test_data_path)
        
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token test-token')
        
        # Test each row
        mape_values = []
        for _, row in test_data.iterrows():
            prediction_data = {
                'location': row['location'],
                'sqft': row['sqft'],
                'bhk': row['bhk'],
                'lift': int(row.get('lift', 0)),
                'parking': int(row.get('parking', 0)),
                'security': int(row.get('security', 0))
            }
            
            response = self.client.post(
                self.predict_url,
                prediction_data,
                format='json'
            )
            
            if response.status_code == status.HTTP_200_OK:
                predicted = response.data['predicted_rent']
                actual = row['actual_rent']
                mape = abs(predicted - actual) / actual * 100
                mape_values.append(mape)
        
        if mape_values:
            avg_mape = np.mean(mape_values)
            self.assertLess(avg_mape, 20.0, "Model MAPE too high")

    def test_concurrent_requests(self):
        """Test system behavior under concurrent requests"""
        import concurrent.futures
        import time
        
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token test-token')
        
        def make_prediction():
            return self.client.post(
                self.predict_url,
                self.prediction_data,
                format='json'
            )
        
        # Make 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_prediction) for _ in range(5)]
            responses = [f.result() for f in futures]
        
        # Check rate limiting worked
        success_count = sum(1 for r in responses if r.status_code == status.HTTP_200_OK)
        throttled_count = sum(1 for r in responses if r.status_code == status.HTTP_429_TOO_MANY_REQUESTS)
        
        self.assertGreater(success_count, 0, "No successful requests")
        self.assertGreater(throttled_count, 0, "No requests were throttled")

    def test_error_responses(self):
        """Test error response formats and messages"""
        
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token test-token')
        
        # Test invalid location
        data = self.prediction_data.copy()
        data['location'] = 'NonexistentCity'
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Test missing required field
        data = self.prediction_data.copy()
        del data['location']
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
        # Test invalid data type
        data = self.prediction_data.copy()
        data['sqft'] = 'not-a-number'
        response = self.client.post(self.predict_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_history_pagination(self):
        """Test prediction history pagination"""
        
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token test-token')
        
        # Create multiple predictions
        for _ in range(25):  # Create more than default page size
            self.client.post(self.predict_url, self.prediction_data, format='json')
        
        # Test first page
        response = self.client.get(f"{self.history_url}?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        # Test last page
        response = self.client.get(f"{self.history_url}?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def tearDown(self):
        """Clean up after each test"""
        self.client.credentials()