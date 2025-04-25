import os
import json
from pathlib import Path
import logging
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Firebase configuration from environment variables
config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL', "")
}

# Initialize Firebase Admin configuration
admin_config = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n') if os.getenv('FIREBASE_PRIVATE_KEY') else None,
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI', "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI', "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', 
                                            "https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": "googleapis.com"
}

# Initialize Pyrebase
try:
    required_config_keys = ['apiKey', 'authDomain', 'projectId']
    missing_keys = [key for key in required_config_keys if not config.get(key)]
    
    if missing_keys:
        raise ValueError(f"Missing required Firebase configuration: {', '.join(missing_keys)}")
    
    firebase = pyrebase.initialize_app(config)
    pyrebase_auth = firebase.auth()
    logger.info("Successfully initialized Pyrebase")
except Exception as e:
    logger.error(f"Failed to initialize Pyrebase: {str(e)}")
    firebase = None
    pyrebase_auth = None

# Initialize Firebase Admin
try:
    # Check if an app is already initialized
    try:
        firebase_admin_app = firebase_admin.get_app()
    except ValueError:
        # Initialize new app if none exists
        required_admin_keys = ['project_id', 'private_key', 'client_email']
        missing_keys = [key for key in required_admin_keys if not admin_config.get(key)]
        
        if missing_keys:
            raise ValueError(f"Missing required Firebase Admin configuration: {', '.join(missing_keys)}")
        
        cred = credentials.Certificate(admin_config)
        firebase_admin_app = firebase_admin.initialize_app(cred)
        logger.info("Successfully initialized Firebase Admin SDK")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
    firebase_admin_app = None