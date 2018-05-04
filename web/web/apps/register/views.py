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
import pyotp

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
        return http.HttpResponseRedirect('/register/password/?uuid=%s' %str(uuid))
    except Exception, inst:
        logger.exception('fail to verify email link: %s' % str(inst))
        return http.HttpResponseServerError()

def show_invalid_link_view(request):
    return render(request, 'register/invalid-link.html', locals())    


def show_password_view(request):
    form = forms.PasswordForm()
    uuid = request.GET['uuid']
    gtoken = pyotp.random_base32()
    gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newton",issuer_name="newton")
    return render(request, 'register/password.html', locals())


@decorators.http_post_required
def submit_password(request):
    try:
        # check uuid
        uuid = request.POST['uuid']
        verification = services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        #check link status
        verification_status = verification.status
        if verification_status != codes.StatusCode.AVAILABLE.value:
            return http.HttpResponseRedirect('/register/invalid-link/')
        email = verification.email_address
        # check form
        gtoken = request.POST['gtoken']
        form = forms.PasswordForm(request.POST)
        if not form.is_valid():
            gtoken = gtoken
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newton",issuer_name="newton")
            return render(request, 'resiter/password.html', locals())
        password = form.cleaned_data['password']
        repassword = form.cleaned_data['repassword']
        # check password
        if password != repassword:
            gtoken = gtoken
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newton",issuer_name="newton")
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Entered passwords differ')])
            return render(request, 'register/password.html', locals())
        # check google authenticator
        gtoken_code = form.cleaned_data['gtoken_code']
        is_pass_google_auth = pyotp.TOTP(gtoken).verify(gtoken_code)
        if not is_pass_google_auth:
            gtoken = gtoken
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newton",issuer_name="newton")
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Google Auth Code Error')])
            return render(request, 'register/password.html', locals())
        username = security.generate_uuid()
        user = User.objects.create_user(username, email)
        user.set_password(password)
        user.save()
        user_profile = user_models.UserProfile.objects.create(user=user)
        user_profile.is_google_authenticator = True
        user_profile.google_authenticator_private_key = gtoken
        user_profile.save()
        # set link valid
        verification.status = codes.StatusCode.CLOSE.value
        verification.save()
        return http.HttpResponseRedirect('/register/register-success/')
    except Exception, inst:
        logger.exception("fail to submit password: %s" % str(inst))
        return http.HttpResponseServerError()


def show_register_success_view(request):
    return render(request, "register/register-success.html", locals())
 
