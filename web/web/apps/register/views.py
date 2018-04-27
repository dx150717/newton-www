# -*- coding: utf-8 -*-
import logging
import datetime

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

import decorators
from config import codes
from utils import http
from utils import security
from user import models as user_models
from . import forms
from . import services

logger = logging.getLogger(__name__)

def show_register_view(request):
    form = forms.EmailForm()
    return render(request, 'register/index.html', locals())

@decorators.http_post_required
def submit_email(request):
    """Submit email to user's inbox
    """
    try:
        form = forms.EmailForm(request.POST)
        if not form.is_valid():
            return render(request, 'register/index.html', locals())
        # check the availablity of email address
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()            
        if user:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Email already existed')])
            return render(request, 'register/index.html', locals())
        is_send_success = services.send_register_validate_email(email, request)
        if not is_send_success:
            return http.HttpResponseRedirect('/register/post-fail/')
        else:
            return http.HttpResponseRedirect('/register/post-success/')
    except Exception, inst:
        logger.exception('fail to submit email: %s' % str(inst))
        return http.HttpResponseServerError()

def show_post_email_success_view(request):
    return render(request, 'register/post-success.html', locals())

def show_post_email_fail_view(request):
    return render(request, 'register/post-fail.html', locals())

def verify_email_link(request):
    try:
        uuid = request.GET['uuid']
        verification = services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        email = verification.email_address
        expire_time = verification.expire_time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        # check whether the given link is expired
        if now > expire_time:
            return http.HttpResponseRedirect('/register/invalid-link/')
        # create user
        username = security.generate_uuid()
        user = User.objects.create_user(username, email)
        user.set_password(username)
        user.save()
        user_profile = user_models.UserProfile.objects.create(user=user)
        user = authenticate(username=email, password=username)
        login(request, user)
        return http.HttpResponseRedirect('/register/password/')
    except Exception, inst:
        logger.exception('fail to verify email link: %s' % str(inst))
        return http.HttpResponseServerError()

def show_invalid_link_view(request):
    return render(request, 'register/invalid-link.html', locals())    

@login_required
def show_password_view(request):
    form = forms.PasswordForm()
    return render(request, 'register/password.html', locals())

@login_required
@decorators.http_post_required
def submit_password(request):
    try:
        form = forms.PasswordForm(request.POST)
        if not form.is_valid():
            return render(request, 'resiter/password.html', locals())
        user = request.user
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return http.HttpResponseRedirect('/user/')
    except Exception, inst:
        logger.exception("fail to submit password: %s" % str(inst))
        return http.HttpResponseServerError()
 
