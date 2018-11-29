"""Settings for testing zinnia on Postgres"""
from events.tests.implementations.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'events',
        'USER': 'postgres',
        'HOST': 'localhost'
    }
}
