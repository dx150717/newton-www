# -*- coding: utf-8 -*-
import os
import logging
from importlib import import_module

from django.conf import settings
from django.core.cache import cache
from django.contrib.sessions.models import Session

logger = logging.getLogger(__name__)
SSO_KEY = 'sso-key'

def get_session(user_id):
    """Query the session by given user ID

    """
    try:
        key = '%s-%s' % (SSO_KEY, user_id)
        v = cache.get(key)
        if v:
            return v
        return None
    except Exception, inst:
        logger.exception("fail to get session:%s" % str(inst))
        return None

def delete_session(session_key, user_id):
    """Delete session by user ID

    """
    try:        
        key = '%s-%s' % (SSO_KEY, user_id)
        cache.delete(key)
    except Exception, inst:
        logger.exception("fail to delete session:%s" % str(inst))

def save_session(user_id, session_key):
    """Save the mapping relation between session_key and user_id

    """
    try:
        key = '%s-%s' % (SSO_KEY, user_id)
        cache.set(key, session_key, settings.SESSION_COOKIE_AGE)
    except Exception, inst:
        logger.exception("fail to save session:%s" % str(inst))
