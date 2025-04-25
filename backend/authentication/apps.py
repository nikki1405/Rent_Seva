from django.apps import AppConfig
import firebase_admin
from django.conf import settings


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        try:
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CONFIG)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
