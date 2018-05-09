# -*- coding: utf-8 -*-
import logging
import os
from enum import Enum
import hashlib
from django.conf import settings
from django.core.cache import cache

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

def delete_session(session_key):
    """Delete session by user ID

    """
    try:
        key = '%s-%s' % (SSO_KEY, user_id)
        cache.delete(key)

        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        s = SessionStore(session_key=session_key)
        s.delete()
    except Exception, inst:
        logger.exception("fail to delete session:%s" % str(inst))

def save_session(user_id, session_id):
    """Save the mapping relation between session_id and user_id

    """
    try:
        key = '%s-%s' % (SSO_KEY, user_id)
        cache.set(key, session_id, settings.SESSION_COOKIE_AGE)
    except Exception, inst:
        logger.exception("fail to save session:%s" % str(inst))
