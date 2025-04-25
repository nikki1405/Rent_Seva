from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def api_home(request):
    """
    API Home endpoint that provides API documentation and version information.
    
    Returns:
        Response: API documentation and version information
    """
    try:
        api_info = {
            "message": "Welcome to RentSeva Prediction API",
            "version": "1.1",
            "endpoints": {
                "auth": {
                    "base_url": "/auth",
                    "endpoints": {
                        "signup": {
                            "url": "/auth/signup/",
                            "method": "POST",
                            "description": "Create a new user account"
                        },
                        "login": {
                            "url": "/auth/login/",
                            "method": "POST",
                            "description": "Authenticate user and get tokens"
                        },
                        "refresh": {
                            "url": "/auth/refresh-token/",
                            "method": "POST",
                            "description": "Refresh expired access token"
                        },
                        "logout": {
                            "url": "/auth/logout/",
                            "method": "POST",
                            "description": "Logout and invalidate tokens"
                        }
                    }
                },
                "predictions": {
                    "base_url": "/api",
                    "endpoints": {
                        "predict": {
                            "url": "/api/predict/",
                            "method": "POST",
                            "description": "Get rent prediction for a property",
                            "authentication": "Required",
                            "rate_limit": {
                                "burst": "10 per minute",
                                "sustained": "100 per day"
                            }
                        },
                        "history": {
                            "url": "/api/history/",
                            "method": "GET",
                            "description": "Get prediction history",
                            "authentication": "Required",
                            "pagination": "Supported"
                        }
                    }
                }
            },
            "features": {
                "v1.1": {
                    "advanced_filters": settings.API_V1_1_SETTINGS['ENABLE_ADVANCED_FILTERS'],
                    "confidence_scores": True,
                    "similar_properties": True
                }
            }
        }
        
        return Response(api_info)
        
    except Exception as e:
        logger.error(f"Error in api_home: {str(e)}")
        return Response({
            "message": "Welcome to Rent Prediction API",
            "status": "error",
            "error": "Error fetching API documentation"
        })
