#-*- coding: utf-8 -*-
import logging
import datetime
import requests
import json

from django.conf import settings
from django.shortcuts import render,redirect
from django.core.validators import validate_email
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.template import Template, Context, loader
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc
from django.forms.forms import NON_FIELD_ERRORS
from django.utils import translation
import pyotp
from ishuman import services as ishuman_services

import decorators
from config import codes
from utils import http
from utils import exception
from utils import security
from user import models as user_models
from . import forms
from . import services

logger = logging.getLogger(__name__)

@decorators.nologin_required
def show_gtoken_view(request):
    try:
        email = request.session.get('email')
        password = request.session.get('password')
        auth_token = request.session.get('auth_token')
        uuid = request.session.get('uuid')
        # check whether session is expired
        if not (email and password and auth_token and uuid):
            return http.HttpResponseRedirect("/register/")
        gtoken = pyotp.random_base32()
        gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
        form = forms.GtokenForm()
        return render(request, 'register/gtoken.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" % str(inst))
        raise exception.SystemError500()

@decorators.nologin_required
@decorators.http_post_required
def submit_gtoken(request):
    try:
        # check whether post data is valid
        form = forms.SubmitGtokenForm(request.POST)
        if not form.is_valid():
            form = forms.GtokenForm()
            return http.HttpResponseRedirect("/register/gtoken/")
        # check uuid
        uuid = form.cleaned_data["uuid"]
        verification = services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        # check google auth
        gtoken = form.cleaned_data["gtoken"]
        gtoken_code = form.cleaned_data["gtoken_code"]
        is_pass_google_auth = pyotp.TOTP(gtoken).verify(gtoken_code)
        if not is_pass_google_auth:
            gtoken = pyotp.random_base32()
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Google Authenticator Code Error')])
            form = forms.GtokenForm()
            return render(request, 'register/gtoken.html', locals())
        # check whether form data is untouched
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        auth_token = form.cleaned_data["auth_token"]
        uuid = form.cleaned_data["uuid"]
        session_email = request.session.get('email')
        session_password = request.session.get('password')
        session_token = request.session.get('auth_token')
        session_uuid = request.session.get('uuid')
        if session_email != email:
            raise exception.SystemError500()
        if session_password != password:
            raise exception.SystemError500()
        if session_token != auth_token:
            raise exception.SystemError500()
        if session_uuid != uuid:
            raise exception.SystemError500()
        #create user
        username = security.generate_uuid()
        user = User.objects.create_user(username, email)
        user.set_password(password)
        user.save()
        user_profile = user_models.UserProfile.objects.create(user=user)
        user_profile.is_google_authenticator = True
        user_profile.google_authenticator_private_key = gtoken
        user_profile.language_code = translation.get_language()
        user_profile.save()
        # set link valid
        verification.status = codes.StatusCode.CLOSE.value
        verification.save()
        # clear session
        if session_token:
            del request.session['auth_token']
        if session_email:
            del request.session['email']
        if session_password:
            del request.session['password']
        if session_uuid:
            del request.session['uuid']
        return http.HttpResponseRedirect('/register/success/')
    except Exception,inst:
        logger.exception("fail to post gtoken:%s" %str(inst))
        raise exception.SystemError500()
