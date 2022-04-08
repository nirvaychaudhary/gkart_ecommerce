import os
from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sgcjxm6nj#15(xh^xb6#9iu$d$f3-q)^62=vyk0n3ey!i8+-ad'
# SECURITY WARNING: don't run with debug turned on in production!



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'db_gkart', 
#         'USER': 'admin', 
#         'PASSWORD': 'admin1234',
#         'HOST': '127.0.0.1', 
#         'PORT': '5432',
#     }
# }

# email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nirvayachaudhary6145ns@gmail.com'
EMAIL_HOST_PASSWORD = 'caliana789'
EMAIL_USE_TLS = True

DEBUG=True
