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

@login_required
def show_set_gtoken_view(request):
    """Show the set google authenticator page
    """
    try:
        redirect_url = request.GET.get('redirect_url')
        gtoken = pyotp.random_base32()
        gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
        form = forms.GtokenForm()
        # save the gtoken in session
        request.session['gtoken'] = gtoken
        return render(request, 'setting/set-gtoken.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" % str(inst))
        raise exception.SystemError500()

@login_required
def show_check_gtoken_view(request):
    """Show the checking google authenticator page
    """
    try:
        redirect_url = request.GET.get('redirect_url')
        if request.method == 'POST':
            form = forms.GtokenForm(request.POST)
            if form.is_valid():
                gtoken_code = form.cleaned_data["gtoken_code"]
                is_pass_google_auth = pyotp.TOTP(request.user.userprofile.google_authenticator_private_key).verify(gtoken_code)
                if is_pass_google_auth:
                    request.session['google_authenticator'] = True
                    return redirect(redirect_url)
                else:
                    form._errors[NON_FIELD_ERRORS] = form.error_class([_('Google Authenticator Code Error')])
        else:
            form = forms.GtokenForm()            
        return render(request, 'setting/check-gtoken.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" % str(inst))
        raise exception.SystemError500()

@login_required
def submit_gtoken(request):
    try:
        # check whether the current user already set the google authenticator
        user_profile = request.user.userprofile
        if user_profile.is_google_authenticator:
            raise Exception("is_google_authenticator is already true.")
        # check whether post data is valid
        form = forms.SubmitGtokenForm(request.POST)
        if not form.is_valid():
            raise Exception("fail to validate")
        # redirect url
        redirect_url = form.cleaned_data['redirect_url']
        if not redirect_url:
            raise Exception("redirect url is null")
        # check google auth
        gtoken = request.session["gtoken"]
        gtoken_code = form.cleaned_data["gtoken_code"]
        is_pass_google_auth = pyotp.TOTP(gtoken).verify(gtoken_code)
        if not is_pass_google_auth:
            raise Exception('is_pass_google_auth is false')
        #create user
        user_profile.is_google_authenticator = True
        user_profile.google_authenticator_private_key = gtoken
        user_profile.save()
        return http.JsonSuccessResponse({'redirect_url': redirect_url})
    except Exception,inst:
        logger.exception("fail to post gtoken:%s" % str(inst))
        return http.JsonErrorResponse(error_message=unicode(_('Google Authenticator Code Error')))
