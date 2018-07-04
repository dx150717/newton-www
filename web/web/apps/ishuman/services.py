# -*- coding: utf-8 -*-
"""The API of ishuman module
"""
import logging
import requests
import json

from django.core.cache import cache
from django.conf import settings

from utils import new_captcha
from utils import security
from utils import http

logger = logging.getLogger(__name__)
CACHE_KEY_PREFIX = 'ishuman-'

def set_captcha(session_key, code):
    """Save the captcha to cache
    """
    try:
        key = '%s%s' % (CACHE_KEY_PREFIX, session_key)
        cache.set(key, code, settings.SESSION_COOKIE_AGE)
    except Exception, inst:
        logger.exception("fail to save captcha:%s" % str(inst))

def get_captcha(session_key):
    """get the captcha code
    """
    try:
        key = '%s%s' % (CACHE_KEY_PREFIX, session_key)
        return cache.get(key)
    except Exception, inst:
        logger.exception("fail to get captcha:%s" % str(inst))
        return None

def refresh_captcha(session_key):
    """Refresh captcha
    """
    try:
        code = security.generate_uuid()[0:5]
        set_captcha(session_key, code)
        return True
    except Exception, inst:
        logger.exception("fail to refresh captcha:%s" % str(inst))
        return False

def is_valid_captcha(request):
    """Check whether it is valid captcha
    """
    try:
        captcha_service_type = request.POST.get('captcha_service_type')
        if captcha_service_type == "google":
            if is_valid_google_recaptcha(request):
                return True
            else:
                return False
        elif captcha_service_type == "tencent":
            if is_valid_tencent_captcha(request):
                return True
            else:
                return False
        else:
            raise Exception("invalid captcha_service_type")
    except Exception, inst:
        logger.exception("fail to check captcha:%s" % str(inst))
        return False

def is_valid_google_recaptcha(request):
    """Check whether it is valid google recaptcha
    """
    try:
        g_recaptcha_response = request.POST.get('google_recaptcha_name')
        if not g_recaptcha_response:
            return False
        post_data = {"secret":settings.GOOGLE_SECRET_KEY, "response":g_recaptcha_response}
        res = requests.post(settings.GOOGLE_VERIFICATION_URL, post_data)
        res = json.loads(res.text)
        if not res['success']:
            return False
        return True
    except Exception, inst:
        logger.exception("fail to check google recaptcha:%s" % str(inst))
        return False


def is_valid_tencent_captcha(request):
    """Check whether it is valid tencent captcha
    """
    try:
        url = settings.TENCENT_CAPTCHA_URL
        ticket = request.POST.get('ticket')
        randstr = request.POST.get('randstr')
        post_data = {
            'aid': settings.TENCENT_CAPTCHA_APP_ID,
            'AppSecretKey': settings.TENCENT_CAPTCHA_APP_SECRET,
            'Ticket': ticket,
            'Randstr': randstr,
            'UserIP': http.get_client_ip(request),
        }
        res = requests.post(url, post_data)
        res = json.loads(res.text)
        if int(res['response']) == 1:
            return True
        return False
    except Exception, inst:
        logger.exception("fail to check tencent captcha:%s" % str(inst))
        return False
