from .base import *

import os
import environ
import django_heroku

env = environ.Env(
    DEBUG=(bool, False),
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET'),
}

# RazorPay configs
RAZOR_KEY_ID = env('RAZOR_KEY_ID')
RAZOR_KEY_SECRET = env('RAZOR_KEY_SECRET')


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db(),
}
DATABASES['default']['CONN_MAX_AGE'] = 60

# Whitenoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
MEDIA_URL = '/evolves/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Activate Django-Heroku.
django_heroku.settings(locals(), staticfiles=False)