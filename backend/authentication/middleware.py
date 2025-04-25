from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from .firebase_config import firebase_admin_app
from .models import FirebaseUser
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class FirebaseAuthMiddleware:
    """
    Middleware to handle Firebase authentication in Django.
    
    This middleware intercepts incoming requests, verifies Firebase ID tokens,
    and attaches the authenticated user to the request object. It handles various
    authentication scenarios and edge cases, providing detailed error logging.
    
    The middleware will:
    1. Extract the Firebase ID token from the Authorization header
    2. Verify the token with Firebase Admin SDK
    3. Create a FirebaseUser instance and attach it to the request
    4. Handle various authentication failure scenarios gracefully
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request through the middleware.
        
        Args:
            request: The incoming HTTP request
            
        Returns:
            The response from the next middleware or view
        """
        request.user = AnonymousUser()
        
        # Skip authentication for paths that don't require it
        if self._should_skip_auth(request.path):
            return self.get_response(request)
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            logger.debug("No Authorization header present")
            return self.get_response(request)
            
        try:
            # Extract and verify the token
            token = self._extract_token(auth_header)
            if token:
                firebase_user = self._verify_token(token)
                if firebase_user:
                    request.user = firebase_user
                    logger.debug("Successfully authenticated user: %s", firebase_user.uid)
                    
        except AuthenticationFailed as e:
            logger.warning("Authentication failed: %s", str(e))
            # Continue processing but with anonymous user
            
        except Exception as e:
            logger.error("Unexpected authentication error: %s", str(e))
            # Continue processing but with anonymous user
            
        return self.get_response(request)

    def _should_skip_auth(self, path):
        """
        Determine if authentication should be skipped for a path.
        
        Args:
            path: str, The request path
            
        Returns:
            bool: True if auth should be skipped, False otherwise
        """
        # Skip authentication for admin and static/media paths
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/api/auth/login/',
            '/api/auth/signup/',
            '/api/auth/refresh/'
        ]
        return any(path.startswith(prefix) for prefix in skip_paths)

    def _extract_token(self, auth_header):
        """
        Extract the token from the Authorization header.
        
        Args:
            auth_header: str, The Authorization header value
            
        Returns:
            str: The extracted token, or None if invalid
            
        Raises:
            AuthenticationFailed: If the header format is invalid
        """
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Invalid Authorization header format. Use Bearer token')
            
        return parts[1]

    def _verify_token(self, token):
        """
        Verify the Firebase ID token and create a FirebaseUser.
        
        Args:
            token: str, The Firebase ID token to verify
            
        Returns:
            FirebaseUser: The authenticated user instance
            
        Raises:
            AuthenticationFailed: If token verification fails
        """
        try:
            # Verify the token with Firebase
            decoded_token = auth.verify_id_token(
                token, 
                app=firebase_admin_app,
                check_revoked=True
            )
            
            # Create FirebaseUser instance
            return FirebaseUser(
                uid=decoded_token['uid'],
                email=decoded_token.get('email')
            )
            
        except auth.RevokedIdTokenError:
            logger.warning("Token has been revoked")
            raise AuthenticationFailed('Token has been revoked')
            
        except auth.ExpiredIdTokenError:
            logger.warning("Token has expired")
            raise AuthenticationFailed('Token has expired')
            
        except auth.InvalidIdTokenError:
            logger.warning("Token is invalid")
            raise AuthenticationFailed('Invalid token')
            
        except Exception as e:
            logger.error("Token verification error: %s", str(e))
            raise AuthenticationFailed('Token verification failed')