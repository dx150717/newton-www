# -*- coding: utf-8 -*-
import logging

from django.core.cache import cache

from utils import http

logger = logging.getLogger(__name__)

def check_session_auth(request):
    try:
        session_key = request.GET.get('sid')
        cache_key = 'django.contrib.sessions.cache' + session_key
        if cache.get(cache_key):
            return http.JsonSuccessResponse()
        return http.JsonErrorResponse()
    except Exception, inst:
        logger.exception("fail to check session auth:%s" % str(inst))
        return http.JsonErrorResponse()

