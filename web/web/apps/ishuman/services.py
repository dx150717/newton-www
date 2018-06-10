# -*- coding: utf-8 -*-
"""The API of ishuman module
"""
import logging

from django.core.cache import cache
from django.conf import settings

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
