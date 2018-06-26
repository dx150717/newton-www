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
from django.utils.translation import ugettext as _
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
from register import services as register_services

logger = logging.getLogger(__name__)

@decorators.nologin_required
def show_register_view(request):
    form = forms.EmailForm()
    return render(request, 'register/index.html', locals())

@decorators.nologin_required
@decorators.http_post_required
def submit_email(request):
    """Submit email to user's inbox
    """
    try:
        form = forms.EmailForm(request.POST)
        if not form.is_valid():
            return render(request, 'register/index.html', locals())
        code = request.POST.get('code')
        if not ishuman_services.is_valid_captcha(request.session.session_key, code):
            form._errors[NON_FIELD_ERRORS] = form.error_class([_("Captcha Error")])
            return render(request, 'register/index.html', locals())
        # check the availablity of email address
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Email already existed')])
            return render(request, 'register/index.html', locals())
        is_send_success = register_services.send_register_validate_email(email, request)
        if not is_send_success:
            return http.HttpResponseRedirect('/register/email/fail/')
        else:
            return http.HttpResponseRedirect('/register/email/success/')
    except Exception, inst:
        logger.exception('fail to submit email: %s' % str(inst))
        raise exception.SystemError500()

def show_post_email_success_view(request):
    return render(request, 'register/post-success.html', locals())

def show_post_email_fail_view(request):
    return render(request, 'register/post-fail.html', locals())

@decorators.nologin_required
def verify_email_link(request):
    try:
        uuid = request.GET.get('uuid')
        verification = register_services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
            #check link status
        verification_status = verification.status
        if verification_status != codes.StatusCode.AVAILABLE.value:
            return http.HttpResponseRedirect('/register/invalid-link/')
        email = verification.email_address
        expire_time = verification.expire_time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        # check whether the given link is expired
        if now > expire_time:
            return http.HttpResponseRedirect('/register/invalid-link/')
        user = User.objects.filter(email=email).first()
        if user:
            verification.status = codes.StatusCode.CLOSE.value
            verification.save()
            return http.HttpResponseRedirect('/register/invalid-link/')
        return http.HttpResponseRedirect('/register/password/?uuid=%s' % str(uuid))
    except Exception, inst:
        logger.exception('fail to verify email link: %s' % str(inst))
        raise exception.SystemError500()

def show_invalid_link_view(request):
    return render(request, 'register/invalid-link.html', locals())    

@decorators.nologin_required
def show_password_view(request):
    try:
        form = forms.PasswordForm()
        uuid = request.GET.get('uuid')
        if not uuid:
            return http.HttpResponseRedirect('/register/invalid-link/')
        verification = register_services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        return render(request, 'register/password.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" % str(inst))
        raise exception.SystemError500()

@decorators.nologin_required
@decorators.http_post_required
def submit_password(request):
    try:
        # check uuid
        uuid = request.POST['uuid']
        verification = register_services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        #check link status
        verification_status = verification.status
        if verification_status != codes.StatusCode.AVAILABLE.value:
            return http.HttpResponseRedirect('/register/invalid-link/')
        email = verification.email_address
        # check form 
        form = forms.PasswordForm(request.POST)
        if not form.is_valid():
            return render(request, 'register/password.html', locals())
        # check password
        password = form.cleaned_data['password']
        repassword = form.cleaned_data['repassword']
        if password != repassword:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Entered passwords do not match')])
            return render(request, 'register/password.html', locals())
        # create user
        username = security.generate_uuid()
        language_code = translation.get_language()
        if not register_services.create_user(username, email, password, language_code, verification):
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Fail to register')])
            return render(request, 'register/password.html', locals())            
        return http.HttpResponseRedirect("/register/success/")
    except Exception,inst:
        logger.exception("fail to post password:%s" % str(inst))
        raise exception.SystemError500()

def show_register_success_view(request):
    return render(request, "register/register-success.html", locals())
 
