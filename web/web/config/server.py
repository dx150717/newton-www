# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """  """

import os
import datetime
from . import codes

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newton',
        'USER': 'root',
        'PASSWORD': ''
    },
    'tokenexchange': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tokenexchange',
        'USER': 'root',
        'PASSWORD': ''
    }
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

# Email settings
EMAIL_BACKEND = 'email_log.backends.EmailBackend'
FROM_EMAIL = 'Newton Project Team<no-reply@crm.newtonproject.org>'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAJIDOOT3MOAE6DSIA'
EMAIL_HOST_PASSWORD = 'As9XbddNsFQu3WApE48QfYdYOTL00KuAbht9lR2EMF7S'
EMAIL_USE_TLS = True

# celery settings
import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/%s' % REDIS_DB_GLOBAL_WORKER
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/%s' % REDIS_DB_GLOBAL_WORKER
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_IMPORTS = ('tasks.task_email', 'tasks.task_blockchain')

from celery.schedules import crontab
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'report-task-free-resource': {
        'task': 'tasks.task_blockchain.sync_blockchain_data',
        'schedule': crontab(minute='*/30'),
    },
}

CHINA_COUNTRY_CALLING_CODE = '86'
# wallet settings
BTC_WALLET_ADDRESS_FILE = 'btc-wallet.txt'
ELA_WALLET_ADDRESS_FILE = 'ela-wallet.txt'

# fund settings
CURRENT_FUND_PHASE = codes.FundPhase.PRIVATE.value
FUND_START_DATE = datetime.datetime(2018, 4, 29, 0, 0)
FUND_END_DATE = datetime.datetime(2018, 5, 30, 0, 0)
FUND_CONFIG = {
    codes.FundPhase.PRIVATE.value: {
        'start_date': '2018-05-07',
        'end_date': '2018-07-20',
        'ela_ratio': 1000,
        'min_ela': 100,
        'btc_ratio': 100000,
        'min_btc': 1,
        'kyc_deadline': '2018-07-20',
        'total_amount_btc': 2500,
        'total_amount_ela': 2500,
    },
    codes.FundPhase.PUBLIC.value: {
        'start_date': '2018-06-01',
        'end_date': '2018-06-10',
        'ela_ratio': 1000,
        'min_ela': 100,
        'btc_ratio': 100000,
        'min_btc': 1,
        'kyc_deadline': '2018-05-20',
        'total_amount_btc': 2500,
        'total_amount_ela': 2500,
    },
}