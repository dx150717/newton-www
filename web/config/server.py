# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

import os
import datetime
from . import codes

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = 'http://www.newtonproject.dev.diynova.com/static/'
STATIC_ROOT = 'web/static'

# website meta
SITE_ID = '1'
BASE_NAME = 'www'

# domain settings
DEBUG = False
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False
DOMAIN = 'www.newtonproject.dev.diynova.com'
BASE_URL = 'http://www.newtonproject.dev.diynova.com'
MEDIA_URL = 'http://www.newtonproject.dev.diynova.com/filestorage/'
MEDIA_ROOT = '/data/newton-storage/filestorage'

#session settings
SESSION_COOKIE_AGE = 7200
SESSION_COOKIE_DOMAIN = '.newtonproject.dev.diynova.com'
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
LOGGING_LEVEL = 'INFO'
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
            'handlers': ['syslog', ],
            'level': LOGGING_LEVEL,
        },
        'django': {
            'handlers': ['syslog', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        },
        'celery.task': {
            'handlers': ['syslog', ],
            'propagate': True,
            'level': LOGGING_LEVEL,
        }
    }
}

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newton_www',
        'USER': 'newton',
        'PASSWORD': 'newton',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'tokenexchange': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tokenexchange',
        'USER': 'newton',
        'PASSWORD': 'newton',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Cache
DEFAULT_CACHE_DB = 3
WORKER_CACHE_DB = 2
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
# Email settings
EMAIL_BACKEND = 'email_log.backends.EmailBackend'
FROM_EMAIL = 'Newton<18735404398@163.com>'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '18735404398@163.com'
EMAIL_HOST_PASSWORD = 'wxf52lol...'
EMAIL_USE_TLS = False
# captcha settings
GOOGLE_SITE_KEY = '6Ld-QWIUAAAAAJRyYXoyyLBXJEC92kpDHGunlq0J'
GOOGLE_SECRET_KEY = '6Ld-QWIUAAAAAAkw-g4sXz_DNmQypWRgq74zH6ON'
TENCENT_CAPTCHA_APP_ID = '2024652208'
TENCENT_CAPTCHA_APP_SECRET = '0KtYZeFMIKEPnx6D8RVeW3w**'
# multiple domain
NEWTON_WEB_URL = 'http://www.newtonproject.dev.diynova.com'
NEWTON_HOME_URL = 'http://home.newtonproject.dev.diynova.com'
NEWTON_GRAVITY_URL = 'http://gravity.newtonproject.dev.diynova.com'
# countdown
FUND_START_DATE = datetime.datetime(2018, 8, 31, 0, 0)
# webpush settings
WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": "BOLsFn4JNe1-TxWNrqgfgrLkPL-EzOQkbPDp8nAh2OODPdOpOkZs8Dwnp4x_IOqpA2uCnYxbaMkz9hkulQbsVc8",
   "VAPID_PRIVATE_KEY": "7ugDH4XCD-NoE1p8vGg8Wy_uAvVAT61PzyX0_nOoVWM",
   "VAPID_ADMIN_EMAIL": "xiawu@diynova.com"
}
# internal service
INTERNAL_API_HOST_IP = '127.0.0.1'
INTERNAL_API_HOST_PORT = '9090'
# newpay download url
NEWPAY_FOR_ANDROID_ALI_DOWNLOAD_URL = "https://newton-release.oss-cn-beijing.aliyuncs.com/newpay-0.2-50-WWWRelease-201812171848.apk"
NEWPAY_FOR_ANDROID_ALI_SG_DOWNLOAD_URL = "https://newton-release-sg.oss-ap-southeast-1.aliyuncs.com/newpay-0.2-50-WWWRelease-201812171848.apk"
NEWTON_NEWPAY_ANDROID_URL = ""
NEWTON_NEWPAY_IOS_URL = ""
