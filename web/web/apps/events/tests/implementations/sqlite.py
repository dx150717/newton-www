"""Settings for testing zinnia on SQLite"""
from events.tests.implementations.settings import *  # noqa

DATABASES = {
    'default': {
        'NAME': 'events.db',
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
