from settings_beta import *

STATIC_URL = 'http://gravity.newtonproject.beta.diynova.com/static/'
DOMAIN = 'gravity.newtonproject.beta.diynova.com'
BASE_URL = 'http://gravity.newtonproject.beta.diynova.com'
MEDIA_URL = 'http://gravity.newtonproject.beta.diynova.com/filestorage/'

LOGGING_API_REQUEST = True
USE_TESTNET = True
ROOT_URLCONF = 'web.urls_gravity'
SESSION_COOKIE_NAME = 'ngsid'
