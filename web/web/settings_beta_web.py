from settings import *

DEBUG = False
TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = False
STATIC_URL = 'http://web.newtonproject.beta.diynova.com/static/'
DOMAIN = 'web.newtonproject.beta.diynova.com'
BASE_URL = 'http://web.newtonproject.beta.diynova.com'
SESSION_COOKIE_DOMAIN = None
MEDIA_URL = 'http://web.newtonproject.beta.diynova.com/filestorage/'

LOGGING_API_REQUEST = True
USE_TESTNET = True
ROOT_URLCONF = 'web.urls_web'
