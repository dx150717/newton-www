#-*- coding: utf-8 -*-
"""
Django settings for education project.

"""
from config import codes

# import common settings 
from config.common_settings import *
from config.settings_label import *

APPEND_SLASH = True

LOGGING_API_REQUEST = True

STATIC_DEFAULT_VERSION = 381

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

SUPPORT_LANGUAGES = (
    ('id', 'Bahasa Indonesia'),
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('es', 'Español'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
    ('nl', 'Nederlands'),
    ('ro', 'Română'),
    ('tr', 'Türkçe'),
    ('ru', 'Pусский'),
    ('pt', 'Português'),
    ('vi', 'Người việt nam'),
    ('fi', 'Suomalainen'),
    ('ar', 'العربية'),
    ('th', 'ไทย'),
    ('ko', '한국어'),
    ('ja', '日本語'),
    ('zh-cn', '简体中文'))

LANGUAGE_LIST = (
    ("zh", codes.EntryLanguage.CHINESE.value),
    ("en", codes.EntryLanguage.ENGLISH.value),
    ("ko", codes.EntryLanguage.KOREAN.value),
    ("ja", codes.EntryLanguage.JAPANESE.value),
    ("ru", codes.EntryLanguage.RUSSIAN.value),
    ("tr", codes.EntryLanguage.TURKISH.value),
    ("es", codes.EntryLanguage.SPANISH.value),
    ("fr", codes.EntryLanguage.FRENCH.value),
    ("de", codes.EntryLanguage.GERMAN.value),
    ("ar", codes.EntryLanguage.ARABIC.value),
    ("nl", codes.EntryLanguage.NETHERLAND.value),
    ("fi", codes.EntryLanguage.FINNISH.value),
    ("id", codes.EntryLanguage.INDONESIAN.value),
    ("it", codes.EntryLanguage.ITALY.value),
    ("th", codes.EntryLanguage.THAILAND.value),
    ("pt", codes.EntryLanguage.PORTUGUESE.value),
    ("vi", codes.EntryLanguage.VIETNAMESE.value),
    ("ro", codes.EntryLanguage.ROMANIA.value),
)

LANGUAGE_CHOICES = (
    (codes.EntryLanguage.CHINESE.value, "Chinese"),
    (codes.EntryLanguage.ENGLISH.value, "English"),
    (codes.EntryLanguage.KOREAN.value, "Korean"),
    (codes.EntryLanguage.JAPANESE.value, "Japanese"),
    (codes.EntryLanguage.RUSSIAN.value, "Russian"),
    (codes.EntryLanguage.TURKISH.value, "Turkish"),
    (codes.EntryLanguage.SPANISH.value, "Spanish"),
    (codes.EntryLanguage.FRENCH.value, "French"),
    (codes.EntryLanguage.GERMAN.value, "German"),
    (codes.EntryLanguage.ARABIC.value, "Arabic"),
    (codes.EntryLanguage.NETHERLAND.value, "Netherland"),
    (codes.EntryLanguage.FINNISH.value, "Finnish"),
    (codes.EntryLanguage.INDONESIAN.value, "Indonesian"),
    (codes.EntryLanguage.ITALY.value, "Italy"),
    (codes.EntryLanguage.THAILAND.value, "Thailand"),
    (codes.EntryLanguage.PORTUGUESE.value, "Portuguese"),
    (codes.EntryLanguage.VIETNAMESE.value, "Vietnamese"),
    (codes.EntryLanguage.ROMANIA.value, "Romania"),
)
# country settings
COUNTRIES_FIRST = []

# blockchain settings
BTC_MAINNET_EXPLORER = 'https://blockchain.info'
BTC_TESTNET_EXPLORER = 'https://testnet.blockchain.info'
ELA_MAINNET_EXPLORER = 'https://blockchain.elastos.org'
ELA_TESTNET_EXPLORER = 'https://blockchain-beta.elastos.org'

# haystack settings
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

# explorer url
NEWTON_EXPLORER_URL = "https://explorer.newtonproject.org/"

# newpay download url
NEWPAY_FOR_ANDROID_GOOGLE_DOWNLOAD_URL = "https://play.google.com/store/apps/details?id=org.newtonproject.newpay.android.release"
NEWPAY_FOR_IOS_DOWNLOAD_URL = "https://itunes.apple.com/app/newpay/id1439660801"
