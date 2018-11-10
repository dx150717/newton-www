# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

import os
import datetime
from . import codes

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = 'http://localhost:8000/static/'
STATIC_ROOT = 'web/static'

# website meta
SITE_ID = '1'
BASE_NAME = 'www'

# domain settings
DEBUG = True
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False
DOMAIN = 'localhost'
BASE_URL = 'http://localhost:8000'
MEDIA_URL = 'http://localhost:8000/filestorage/'
MEDIA_ROOT = './'

#session settings
SESSION_COOKIE_AGE = 7200
SESSION_COOKIE_DOMAIN = None
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_NAME = 'nwsid'

# LOGGING
import platform
system_string = platform.system()
if system_string == 'Linux':
    syslog_path = '/dev/log'
elif system_string == 'Darwin':
    syslog_path = '/var/run/syslog'
else:
    raise Exception('Upsupport platform!')

from logging.handlers import SysLogHandler
LOGGING_LEVEL = 'DEBUG'
LOGGING_LEVEL_SENTRY = 'ERROR'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s][%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'syslog': {
            'level': LOGGING_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'formatter': 'verbose',
            'address': syslog_path,
        },
        'sentry': {
            'level': LOGGING_LEVEL_SENTRY,
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': LOGGING_LEVEL,
        },
        'django': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'celery.task': {
            'handlers': ['console', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        }
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newton_www',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'tokenexchange': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tokenexchange',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

# Cache
DEFAULT_CACHE_DB = 1
REDIS_DB_GLOBAL_WORKER = 2
REDIS_CACHE_DB = DEFAULT_CACHE_DB
REDIS_CACHE_PASSWORD = ''
REDIS_CACHE_HOST = '127.0.0.1'
REDIS_CACHE_PORT = 6379
REDIS_CACHE_URL = 'redis://%s:%s' % (REDIS_CACHE_HOST, REDIS_CACHE_PORT)
REDIS_WORKER_URL = 'redis://127.0.0.1:6379'
REDIS_LOCAL_GAME_URL = 'redis://127.0.0.1:6379'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "%s/%s" % (REDIS_CACHE_URL, DEFAULT_CACHE_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'products',
    },
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'cumtbliu@163.com'
EMAIL_HOST_PASSWORD = '025103a'
FROM_EMAIL = 'cumtbliu@163.com'
# captcha settings
GOOGLE_SITE_KEY = '6LddrlUUAAAAACpdea_F7GTRBCzkYBoInup9WJPv'
GOOGLE_SECRET_KEY = "6LddrlUUAAAAAJDVSNQcnVsBJeDXSdToo_Gu2qvb"
TENCENT_CAPTCHA_APP_ID = '2075015244'
TENCENT_CAPTCHA_APP_SECRET = '0alyS6l5dhGmH32EX4zIQaw**'
# multiple domain
NEWTON_WEB_URL = 'http://localhost:8000'
NEWTON_HOME_URL = 'http://home.test.newtonproject.org:8000'
NEWTON_GRAVITY_URL = 'http://gravity.test.newtonproject.org:8000'

# celery settings
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/%s' % REDIS_DB_GLOBAL_WORKER
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/%s' % REDIS_DB_GLOBAL_WORKER
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_IMPORTS = ('tasks.task_email', 'tasks.task_blockchain')

# countdown time
FUND_START_DATE = datetime.datetime(2018, 9, 03, 0, 0)


WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": "BMI6CuaoXispCyXjO34kEUcL_MacbKDgXG5xWneXvlDi-mOqyrkaFaZI3PteBB5KgmhspUWTS2rxlwkftwiNHJ4",
   "VAPID_PRIVATE_KEY": "qi48KlUEzaUx_21KPWzgkaVDSyz-IyRLMKXxOPKbaPY",
   "VAPID_ADMIN_EMAIL": "wuwenmin@diynova.com"
}

INTERNAL_API_HOST_IP = '127.0.0.1'
INTERNAL_API_HOST_PORT = '9090'