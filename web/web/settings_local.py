#-*- coding: utf-8 -*-
"""
Django settings for education project.

"""
from config import codes

# import common settings 
from config.common_settings import *
from config.settings_label import *

APPEND_SLASH = False

LOGGING_API_REQUEST = True

STATIC_DEFAULT_VERSION = 290

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

# verification default expire time s
VERIFICATION_DEFAULT_EXPIRE_TIME = 7200

# authenticate settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'backends.auth.EmailAuthBackend',
)
# google recaptcha verification url
GOOGLE_VERIFICATION_URL = "https://www.google.com/recaptcha/api/siteverify"
# tencent captcha
TENCENT_CAPTCHA_URL = 'https://ssl.captcha.qq.com/ticket/verify'
# global authenticate
LOGIN_URL = '/login/'

# page size
PAGE_SIZE = 20

# database router
DATABASE_ROUTERS = ['web.database_router.NewtonRouter']
# database mapping
DATABASE_APPS_MAPPING = {
    "tokenexchange":"tokenexchange",
}


SUPPORT_LANGUAGES = (('id', 'Bahasa Indonesia'), ('de', 'Deutsch'), ('en', 'English'),  ('es', 'Español'), ('fr', 'Français'), ('it', 'Italiano'), ('nl', 'Nederlands'), ('tr', 'Türkçe'), ('ru', 'Pусский'), ('fi', 'suomalainen'), ('ar', 'العربية'), ('th', 'ไทย'), ('ko', '한국어'), ('ja', '日本語'), ('zh-cn', '简体中文'))


# country settings
COUNTRIES_FIRST = []

# blockchain settings
BTC_MAINNET_EXPLORER = 'https://blockchain.info'
BTC_TESTNET_EXPLORER = 'https://testnet.blockchain.info'
ELA_MAINNET_EXPLORER = 'https://blockchain.elastos.org'
ELA_TESTNET_EXPLORER = 'https://blockchain-beta.elastos.org'
