import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *


sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

DEBUG = True

ADMINS = {
    ('Fabrice J', 'fabricejaouen@yahoo.com'),
}

ALLOWED_HOSTS = ['www.papounet-super-diet.fr', 'papounet-super-diet.fr', '104.248.33.242', 'localhost']

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',

    }
}


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')