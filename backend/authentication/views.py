from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .firebase_config import pyrebase_auth
from .models import EstimateHistory
import firebase_admin
from firebase_admin import auth
import logging
import traceback

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not pyrebase_auth:
            logger.error("Firebase Authentication is not properly initialized")
            return Response({
                'error': 'Authentication service is not available'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Authenticate with Firebase
        user = pyrebase_auth.sign_in_with_email_and_password(email, password)
        
        return Response({
            'token': user['idToken'],
            'user': {
                'uid': user['localId'],
                'email': user['email']
            }
        })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        error_message = str(e)
        if 'EMAIL_NOT_FOUND' in error_message:
            return Response({'error': 'Email not found'}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'INVALID_PASSWORD' in error_message:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'INVALID_EMAIL' in error_message:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': 'Authentication failed. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')
        
        # Create user in Firebase
        user = pyrebase_auth.create_user_with_email_and_password(email, password)
        
        # Update display name if provided
        if name:
            auth.update_user(
                user['localId'],
                display_name=name
            )
        
        return Response({
            'token': user['idToken'],
            'user': {
                'uid': user['localId'],
                'email': user['email'],
                'name': name
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        error_message = str(e)
        if 'EMAIL_EXISTS' in error_message:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        return Response({
            'uid': user.uid,
            'email': user.email
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Firebase doesn't have a server-side logout
        # The client should delete the token
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange refresh token for a new ID token
        user = pyrebase_auth.refresh(refresh_token)
        
        return Response({
            'token': user['idToken'],
            'user': {
                'uid': user['userId'],
                'email': user['email']
            }
        })
    except Exception as e:
        error_message = str(e)
        logger.error(f"Token refresh error: {error_message}")
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_estimates_history(request):
    try:
        user_id = request.user.uid
        histories = EstimateHistory.objects.filter(user_id=user_id)
        
        history_data = [{
            'id': history.id,
            'location': history.location,
            'bhk': history.bhk,
            'sqft': history.sqft,
            'predicted_rent': history.predicted_rent,
            'created_at': history.created_at.isoformat()
        } for history in histories]
        
        return Response(history_data)
    except Exception as e:
        logger.error(f"Error fetching estimate history: {str(e)}")
        return Response(
            {'error': 'Failed to fetch estimate history'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
