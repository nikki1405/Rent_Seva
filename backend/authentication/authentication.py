from rest_framework import authentication
from rest_framework import exceptions
from firebase_admin import auth
from .models import FirebaseUser

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        try:
            # Validate Bearer token format
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid authorization header format. Use Bearer token')
                
            token = auth_parts[1]
            # Verify the token
            decoded_token = auth.verify_id_token(token)
            
            # Create a custom user object
            firebase_user = FirebaseUser(
                uid=decoded_token['uid'],
                email=decoded_token.get('email')
            )
            
            # Return tuple of (user, auth)
            return (firebase_user, None)
            
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

    def authenticate_header(self, request):
        return 'Bearer'