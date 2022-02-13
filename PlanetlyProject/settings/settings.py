from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG_MODE'] in ['True', True]

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DATABASE_DEFAULT_NAME'],
        'USER': os.environ['DATABASE_DEFAULT_USER'],
        'PASSWORD': os.environ['DATABASE_DEFAULT_PASSWORD'],
        'HOST': os.environ['DATABASE_DEFAULT_HOST'],
        'PORT': os.environ['DATABASE_DEFAULT_PORT'],
    }
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
