"""Settings for testing zinnia on MySQL"""
from events.tests.implementations.settings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'events',
        'USER': 'root',
        'HOST': 'localhost'
    }
}
