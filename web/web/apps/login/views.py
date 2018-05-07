# -*- coding: utf-8 -*-
import logging
import requests
import json
import urlparse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc
from django.forms.forms import NON_FIELD_ERRORS
import pyotp

import decorators
from utils import http
from utils import security
from . import forms
from user import models as user_models

logger = logging.getLogger(__name__)

def show_login_view(request):
    form = forms.LoginForm()
    next = request.GET.get('next', '')
    return render(request, 'login/index.html', locals())

@decorators.http_post_required
def post_login(request):
    try:
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse(error_message=_("Form Error"))
        g_recaptcha_response = request.POST.get('g-recaptcha-response')
        post_data = {"secret":settings.GOOGLE_SECRET_KEY, "response":g_recaptcha_response}
        res = requests.post(settings.GOOGLE_VERIFICATION_URL, post_data)
        res = json.loads(res.text)
        if not res['success']:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_("No captcha")])
            return http.JsonErrorResponse(error_message=_("Auth Recaptcha Error"))
        # start authenticate
        username = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user or user.is_staff:
            return http.JsonErrorResponse(error_message=_("Email or Password don't match"))
        profile = user_models.UserProfile.objects.filter(user=user).first()
        auth_token = security.generate_uuid()
        request.session['auth_token'] = auth_token
        return http.JsonSuccessResponse(data={"auth_token":auth_token})
    except Exception, inst:
        logger.exception("fail to post login:%s" % str(inst))
        return http.JsonErrorResponse(error_message=_("Request Time Out"))

@decorators.http_post_required
def post_google_authenticator(request):
    try:
        gtoken_code = request.POST['gtoken_code']
        email = request.POST['email']
        passwrod = request.POST['password']
        auth_token = request.POST['auth_token']
        session_token = request.session.get('auth_token')
        # clear the session
        if session_token:
            del request.session['auth_token']
        user = authenticate(username=email, password=passwrod)
        if not user or user.is_staff:
            return http.JsonErrorResponse(error_message=_("no user"))
        user_profile = user_models.UserProfile.objects.filter(user=user).first()
        if not user_profile:
            return http.JsonErrorResponse(error_message=_("no user profile"))
        is_pass_google_auth = pyotp.TOTP(user_profile.google_authenticator_private_key).verify(gtoken_code)
        if not is_pass_google_auth:
            return http.JsonErrorResponse(error_message=_("Google auth error"))
        if True:
            next = request.POST.get('next')
            if next:
                result = urlparse.urlparse(next)
                if result and not result.netloc and result.path:
                    return http.JsonSuccessResponse(data={"msg":next})
            login(request, user)
            return http.JsonSuccessResponse(data={"msg":"/user/"})
        else:
            return http.JsonUnauthErrorResponse()
    except Exception, inst:
        logger.exception("fail to post google authedticator:%s" % str(inst))
        return http.HttpResponseServerError()
