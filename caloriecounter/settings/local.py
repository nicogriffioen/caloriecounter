from .base import *

SITE_URL = "http://127.0.0.1:8000"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'caloriecounter',
        'USER': 'caloriecounter',
        'PASSWORD': 'caloriecounter',
        'HOST': 'localhost',
        'PORT': '',
    }
}