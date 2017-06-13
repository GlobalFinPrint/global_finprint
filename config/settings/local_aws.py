# -*- coding: utf-8 -*-
from boto.s3.connection import OrdinaryCallingFormat

from .common import *


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

# cross-domain
# CORS_ORIGIN_ALLOW_ALL = True

# CACHING
# ------------------------------------------------------------------------------
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': ''
#     }
# }

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False  # don't add complex authentication-related query parameters for requests
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME", default='finprint-videos-test')
AWS_AUTO_CREATE_BUCKET = True
