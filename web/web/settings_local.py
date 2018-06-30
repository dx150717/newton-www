#-*- coding: utf-8 -*-
"""
Django settings for education project.

"""
from config import codes

# import common settings 
from config.common_settings import *
from config.settings_label import *

SITE_ID = '1'
APPEND_SLASH = False

LOGGING_API_REQUEST = True

STATIC_DEFAULT_VERSION = 243

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'context_processors.settings_variable',
)


SESSION_COOKIE_AGE = 5400
SESSION_COOKIE_DOMAIN = '.newtonproject.org'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# website meta
BASE_NAME = 'newtonproject'

# verification default expire time s
VERIFICATION_DEFAULT_EXPIRE_TIME = 7200

# authenticate settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'backends.auth.EmailAuthBackend',
)
# google recaptcha verification url
GOOGLE_VERIFICATION_URL = "https://www.google.com/recaptcha/api/siteverify"
GOOGLE_SECRET_KEY = "6LddrlUUAAAAAJDVSNQcnVsBJeDXSdToo_Gu2qvb"

# global authenticate
LOGIN_URL = '/login/'

# chain settings of digital currency
USE_TESTNET = False

# page size
PAGE_SIZE = 20

# multiple domain
NEWTON_WEB_URL = 'https://www.newtonproject.org'
NEWTON_HOME_URL = 'https://home.newtonproject.org'
NEWTON_GRAVITY_URL = 'https://gravity.newtonproject.org'

# database router
DATABASE_ROUTERS = ['web.database_router.NewtonRouter']
# database mapping
DATABASE_APPS_MAPPING = {
    "tokenexchange":"tokenexchange",
}


SUPPORT_LANGUAGES = (('en','English'), ('zh-cn','简体中文'), ('ja','日本語'), ('ko','한국어'), ('ru','Pусский'), ('fr', 'France'), ('tr','Türkiye'), ('es','Español'))

# country settings
COUNTRIES_FIRST = []

# blockchain settings
BTC_MAINNET_EXPLORER = 'https://blockchain.info'
BTC_TESTNET_EXPLORER = 'https://testnet.blockchain.info'
ELA_MAINNET_EXPLORER = 'https://blockchain.elastos.org'
ELA_TESTNET_EXPLORER = 'https://blockchain-beta.elastos.org'
