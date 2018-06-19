# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import uuid
import logging
from config import codes
from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse
from django.shortcuts import resolve_url
from django.core.cache import cache
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from utils import security
from utils import http
from config import codes
from config import settings_label

logger = logging.getLogger(__name__)

def http_post_required(func):
    def _decorator(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed('Only POST here')
        return func(request, *args, **kwargs)
    return _decorator

def http_get_required(func):
    def _decorator(request, *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed('Only GET here')
        return func(request, *args, **kwargs)
    return _decorator

def access_required(func):
    def _decorator(request, *args, **kwargs):
        sign = request.POST.get('sign')
        app_key = request.POST.get('app_key')
        if app_key in settings.APP_KEY_TO_SECRET:
            secret = settings.APP_KEY_TO_SECRET[app_key]
        else:
            secret = settings.API_ACCESS_SECRET
        if settings.LOGGING_API_REQUEST:
            logger.debug("request: %s" % str(request.POST))
        signed_string = security.sign_hmac(request.POST, secret=secret)
        if sign == signed_string or (settings.DEBUG and not settings.SECURITY_API_ACCESS_AUTH):
            if settings.CHANGE_SYSTEM_SERVICE_ENABLE:
                status_info = operation_services.get_service_status()
                if status_info.get('status') == codes.SystemServiceStatus.MAINTAIN.value:
                    return http.JsonErrorResponse(codes.ErrorCode.MAINTAIN.value, error_message=status_info.get('msg'), data={'m_time': status_info.get('m_time')})
            response = func(request, *args, **kwargs)
            if settings.LOGGING_API_REQUEST:
                logger.debug("response: %s" % str(response))
            return response
        logger.error("signed_string error!")
        return http.JsonErrorResponse(codes.ErrorCode.SIGN_ERROR.value)
    return _decorator

def auth_required(func):
    def _decorator(request, *args, **kwargs):
        auth_token = request.POST.get('auth_token')
        user = auth_services.check_auth_token(auth_token)
        if user and hasattr(user, 'userprofile'):
            request.user = User.objects.get(id=user.id)
            if request.user.is_active == False:
                return http.JsonErrorResponse(codes.ErrorCode.BLOCK_USER.value)
            return func(request, *args, **kwargs)
        logger.info('auth_required:unauth:POST:%s' % request.POST)
        return http.JsonErrorResponse(codes.ErrorCode.UNAUTH.value)
    return _decorator

def nologin_required(func):
    """Ensure the current user is not login,otherwise redirect to user page
    """
    def _decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            return http.HttpResponseRedirect('/user/')
        return func(request, *args, **kwargs)
    return _decorator

def google_authenticator_required(func):
    """Ensure that the current user is set the google authenticator
    """
    def _decorator(request, *args, **kwargs):
        if request.user.userprofile.is_google_authenticator:
            return func(request, *args, **kwargs)
        return http.HttpResponseRedirect('/setting/gtoken/?redirect_url=' + request.path)
    return _decorator

def check_google_authenticator_session(func):
    """Ensure that the session of google authenticator is not expired
    """
    def _decorator(request, *args, **kwargs):
        if request.session.get('google_authenticator'):
            return func(request, *args, **kwargs)
        return http.HttpResponseRedirect('/setting/gtoken/check/?redirect_url=' + request.path)
    return _decorator

def admin_user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.ADMIN_LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def admin_permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return admin_user_passes_test(check_perms)
