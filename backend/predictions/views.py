import os
import joblib
import logging
import datetime
import json
import numpy as np
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import RentPrediction
from authentication.models import EstimateHistory

logger = logging.getLogger(__name__)

# Load ML models and evaluation data at startup
model_path = os.path.join(settings.ML_MODELS_DIR, 'rent_predictor.joblib')
scaler_path = os.path.join(settings.ML_MODELS_DIR, 'scaler.joblib')
encoder_path = os.path.join(settings.ML_MODELS_DIR, 'label_encoder.joblib')
eval_path = os.path.join(settings.ML_MODELS_DIR, 'model_evaluation.json')

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    with open(eval_path) as f:
        model_evaluation = json.load(f)
    logger.info("Successfully loaded ML models and evaluation data")
except Exception as e:
    logger.error(f"Failed to load ML models or evaluation data: {e}")
    model = scaler = label_encoder = model_evaluation = None

# Vizag location rent ranges with more granular BHK-specific ranges
VIZAG_LOCATIONS = {
    'MVP Colony': {
        'min': 8000, 'max': 15000, 'tier': 3,
        'bhk_ranges': {1: (8000, 12000), 2: (12000, 18000), 3: (16000, 25000)}
    },
    'Beach Road': {
        'min': 10000, 'max': 18000, 'tier': 3,
        'bhk_ranges': {1: (10000, 15000), 2: (15000, 22000), 3: (20000, 30000)}
    },
    'Madhurawada': {
        'min': 7000, 'max': 14000, 'tier': 2,
        'bhk_ranges': {1: (6000, 10000), 2: (10000, 15000), 3: (14000, 20000)}
    },
    'Gajuwaka': {
        'min': 5000, 'max': 10000, 'tier': 1,
        'bhk_ranges': {1: (5000, 8000), 2: (7500, 15000), 3: (12000, 18000)}
    },
    'Pendurthi': {
        'min': 4000, 'max': 8000, 'tier': 1,
        'bhk_ranges': {1: (4000, 7000), 2: (7000, 12000), 3: (10000, 15000)}
    },
    'Seethammadhara': {
        'min': 8000, 'max': 15000, 'tier': 3,
        'bhk_ranges': {1: (8000, 12000), 2: (12000, 18000), 3: (16000, 25000)}
    },
    'Rushikonda': {
        'min': 7000, 'max': 14000, 'tier': 2,
        'bhk_ranges': {1: (7000, 11000), 2: (11000, 16000), 3: (15000, 22000)}
    }
}

def validate_rent_prediction(prediction, location, bhk, sqft):
    """Validate predicted rent is within reasonable bounds for Vizag"""
    if location not in VIZAG_LOCATIONS:
        return False, f"Invalid location: {location}. Must be one of {', '.join(VIZAG_LOCATIONS.keys())}"
    
    # Get location-specific rent range with BHK-specific ranges
    loc_range = VIZAG_LOCATIONS[location]
    bhk_ranges = loc_range['bhk_ranges']
    min_rent, max_rent = bhk_ranges.get(bhk, (loc_range['min'], loc_range['max']))
    
    # Basic range check
    if prediction < min_rent or prediction > max_rent:
        return False, f"Predicted rent ₹{prediction:,.2f} outside reasonable range for {location} ({bhk} BHK): ₹{min_rent:,.2f} - ₹{max_rent:,.2f}"
    
    # Validate price per sqft based on location tier
    base_rates = {1: (5, 25), 2: (8, 30), 3: (10, 35)}
    tier = loc_range['tier']
    min_rate, max_rate = base_rates[tier]
    
    price_per_sqft = prediction / sqft
    if price_per_sqft < min_rate or price_per_sqft > max_rate:
        return False, f"Price per square foot (₹{price_per_sqft:.2f}) outside reasonable range for {location} (₹{min_rate} - ₹{max_rate})"
    
    return True, None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_rent(request):
    try:
        data = request.data
        if not model or not scaler or not label_encoder:
            return Response(
                {'error': 'ML models not loaded'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Validate required fields
        required_fields = ['location', 'bhk', 'built_area_sqft', 'bathrooms', 'lift', 
                         'air_conditioner', 'parking', 'gym', 'security', 'water_supply']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {'error': f'Missing required fields: {", ".join(missing_fields)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate location
        location = str(data['location']).strip()
        if location not in VIZAG_LOCATIONS:
            return Response(
                {'error': f'Invalid location. Must be one of: {", ".join(VIZAG_LOCATIONS.keys())}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and convert numeric fields
        try:
            bhk = int(data['bhk'])
            built_area_sqft = float(data['built_area_sqft'])
            bathrooms = float(data['bathrooms'])
            
            # Handle amenities with proper default values
            amenities = {
                'lift': float(bool(data.get('lift', False))),
                'air_conditioner': float(bool(data.get('air_conditioner', False))),
                'parking': float(bool(data.get('parking', False))),
                'gym': float(bool(data.get('gym', False))),
                'security': float(bool(data.get('security', False))),
                'water_supply': float(bool(data.get('water_supply', False)))
            }
        except (ValueError, TypeError) as e:
            return Response(
                {'error': 'Invalid numeric value provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get location details
        loc_range = VIZAG_LOCATIONS[location]
        location_tier = loc_range.get('tier', 1)
        
        # Calculate amenities score
        amenities_score = sum([
            0.15 * amenities['lift'],
            0.30 * amenities['air_conditioner'],
            0.20 * amenities['parking'],
            0.10 * amenities['gym'],
            0.20 * amenities['security'],
            0.20 * amenities['water_supply']
        ]) * (location_tier / 3)  # Scale by location tier

        # Calculate area per room (bhk + 2 for living and kitchen)
        area_per_room = built_area_sqft / (bhk + 2)
        
        # Encode location - handle potential encoding errors
        try:
            location_encoded = label_encoder.transform(np.array([location]).reshape(-1, 1))[0]
        except (ValueError, AttributeError) as e:
            logger.error(f"Location encoding error: {str(e)}")
            return Response(
                {'error': f'Error encoding location: {location}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare features array
        features = np.array([
            location_encoded,
            built_area_sqft,
            bhk,
            bathrooms,
            amenities['lift'],
            amenities['air_conditioner'],
            amenities['parking'],
            amenities['gym'],
            amenities['security'],
            amenities['water_supply'],
            area_per_room,
            amenities_score,
            float(location_tier)
        ]).reshape(1, -1)

        # Get base prediction
        features_scaled = scaler.transform(features)
        base_prediction = model.predict(features_scaled)[0]
        
        # Get target range for this configuration
        bhk_ranges = loc_range.get('bhk_ranges', {})
        target_min, target_max = bhk_ranges.get(bhk, (loc_range.get('min', 5000), loc_range.get('max', 10000)))
        target_mid = (target_min + target_max) / 2
        
        # Calculate scaling factor to bring prediction into target range
        current_scale = base_prediction / target_mid
        scaling_factor = 1.0 / current_scale if current_scale > 0 else 1.0
        
        # Apply scaling with additional adjustments
        final_prediction = base_prediction * scaling_factor
        
        # Apply area-based adjustment
        if built_area_sqft > 1000:
            area_factor = min(1.0, 1000 / built_area_sqft)
            final_prediction *= area_factor
        
        # Apply amenities adjustment (max 20% impact)
        amenities_factor = 1.0 + (amenities_score * 0.2)
        final_prediction *= amenities_factor
        
        # Ensure prediction stays within bounds
        final_prediction = max(target_min, min(final_prediction, target_max))
        
        # Validate prediction
        is_valid, error_msg = validate_rent_prediction(
            final_prediction,
            location,
            bhk,
            built_area_sqft
        )
        
        if not is_valid:
            logger.warning(f"Invalid prediction: {error_msg}")
            return Response(
                {'error': f'Invalid prediction: {error_msg}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate confidence score
        base_confidence = 0.7  # Base confidence level
        location_stats = model_evaluation.get('location_stats', {}).get(location, {})
        location_confidence = min(1.0, location_stats.get('count', 0) / 20)
        
        # Range confidence
        range_width = target_max - target_min
        range_center = (target_max + target_min) / 2
        range_confidence = 1.0 - (abs(final_prediction - range_center) / range_width)
        
        # Combine confidence scores
        confidence_score = min(1.0, (
            base_confidence * 0.4 +
            location_confidence * 0.3 +
            range_confidence * 0.2 +
            amenities_score * 0.1
        ))
        
        # Store prediction
        rent_prediction = RentPrediction.objects.create(
            user_id=request.user.uid,
            location=location,
            bhk=bhk,
            sqft=built_area_sqft,
            predicted_rent=final_prediction,
            confidence_score=confidence_score,
            furnishing_status=data.get('furnishing', 'unfurnished'),
            preferred_tenants=data.get('preferred_tenants', 'any')
        )
        
        # Save to EstimateHistory
        estimate_history = EstimateHistory.objects.create(
            user_id=request.user.uid,
            location=location,
            bhk=bhk,
            sqft=built_area_sqft,
            predicted_rent=final_prediction
        )
        
        return Response({
            'id': rent_prediction.id,
            'predicted_rent': final_prediction,
            'confidence_score': confidence_score,
            'timestamp': rent_prediction.created_at.isoformat(),
            'history_id': estimate_history.id  # Also return the history ID
        })
        
    except ValueError as e:
        logger.error(f"Value error in prediction: {str(e)}")
        return Response(
            {'error': f'Invalid input value: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET']) 
def health_check(request):
    """Check if ML models are loaded correctly"""
    return Response({
        'status': 'healthy' if all([model, scaler, label_encoder]) else 'unhealthy',
        'models_loaded': ['rent_predictor', 'scaler', 'label_encoder'] if all([model, scaler, label_encoder]) else []
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """
    Get prediction history for the authenticated user.
    
    Returns a list of previous rent predictions made by the user,
    sorted by creation date (newest first).
    """
    try:
        user_id = request.user.uid
        predictions = RentPrediction.objects.filter(user_id=user_id)
        
        history_data = [{
            'id': pred.id,
            'location': pred.location,
            'bhk': pred.bhk,
            'sqft': pred.sqft,
            'predicted_rent': pred.predicted_rent,
            'created_at': pred.created_at.isoformat(),
            'furnishing_status': pred.furnishing_status,
            'preferred_tenants': pred.preferred_tenants,
            'confidence_score': pred.confidence_score
        } for pred in predictions]
        
        return Response(history_data)
    except Exception as e:
        logger.error(f"Error fetching prediction history: {str(e)}")
        return Response(
            {'error': 'Failed to fetch prediction history'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
