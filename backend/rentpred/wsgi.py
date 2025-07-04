"""
WSGI config for rentpred project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentpred.settings')

application = get_wsgi_application()
