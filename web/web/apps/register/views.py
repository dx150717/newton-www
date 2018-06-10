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
        code = form.cleaned_data['code']
        if code != ishuman_services.get_captcha(request.session.session_key):
            return http.JsonErrorResponse(error_message=_("Captcha Error"))
        # check robot 
        # g_recaptcha_response = request.POST.get('g-recaptcha-response')
        # if not g_recaptcha_response:
        #     form._errors[NON_FIELD_ERRORS] = form.error_class([_("No captcha")])
        #     return render(request, 'register/index.html', locals())
        # post_data = {"secret":settings.GOOGLE_SECRET_KEY, "response":g_recaptcha_response}
        # res = requests.post(settings.GOOGLE_VERIFICATION_URL, post_data)
        # res = json.loads(res.text)
        # if not res['success']:
        #     form._errors[NON_FIELD_ERRORS] = form.error_class([_("No captcha")])
        #     return render(request, 'register/index.html', locals())
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
    try:
        form = forms.PasswordForm()
        uuid = request.GET['uuid']
        return render(request, 'register/password.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" %str(inst))
        return http.HttpResponseServerError()


def show_gtoken_view(request):
    try:
        email = request.session.get('email')
        password = request.session.get('password')
        auth_token = request.session.get('auth_token')
        uuid = request.session.get('uuid')
        gtoken = pyotp.random_base32()
        gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
        form = forms.GtokenForm()
        return render(request, 'register/gtoken.html', locals())
    except Exception, inst:
        logger.exception("fail to show gtoken view:%s" %str(inst))
        return http.HttpResponseServerError()

@decorators.http_post_required
def submit_gtoken(request):
    try:
        form = forms.GtokenForm(request.POST)
        if not form.is_valid():
            gtoken = request.POST.get('gtoken')
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
            return render(request, 'register/gtoken.html', locals())
        uuid = request.POST.get('uuid')
        # check uuid
        verification = services.get_register_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/register/invalid-link/')
        # get post params
        email = request.POST.get('email')
        password = request.POST.get('password')
        gtoken = request.POST.get('gtoken')
        auth_token = request.POST.get('auth_token')
        gtoken_code = form.cleaned_data['gtoken_code']
        # check google auth
        is_pass_google_auth = pyotp.TOTP(gtoken).verify(gtoken_code)
        if not is_pass_google_auth:
            gtoken = gtoken
            gtoken_uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newtonproject.org")
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Google Authenticator Code Error')])
            return render(request, 'register/gtoken.html', locals())
        # clear session
        session_email = request.session.get('email')
        session_password = request.session.get('password')
        session_token = request.session.get('auth_token')
        session_uuid = request.session.get('uuid')
        if session_token:
            del request.session['auth_token']
        if session_email:
            del request.session['email']
        if session_password:
            del request.session['password']
        if session_uuid:
            del request.session['uuid']
        if session_email != email:
            return http.HttpResponseServerError()
        if session_password != password:
            return http.HttpResponseServerError()
        if session_token != auth_token:
            return http.HttpResponseServerError()
        if session_uuid != uuid:
            return http.HttpResponseServerError()
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
        return http.HttpResponseRedirect('/register/register-success/')
    except Exception,inst:
        logger.exception("fail to post gtoken:%s" %str(inst))
        return http.HttpResponseServerError()

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
        form = forms.PasswordForm(request.POST)
        if not form.is_valid():
            return render(request, 'register/password.html', locals())
        # check password
        password = form.cleaned_data['password']
        repassword = form.cleaned_data['repassword']
        if password != repassword:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_('Entered passwords do not match')])
            return render(request, 'register/password.html', locals())
        request.session['email'] = email
        request.session['password'] = password
        request.session['auth_token'] = security.generate_uuid()
        request.session['uuid'] = uuid
        return http.HttpResponseRedirect("/register/gtoken/")
    except Exception,inst:
        logger.exception("fail to post password:%s" %str(inst))
        return http.HttpResponseServerError()


def show_register_success_view(request):
    return render(request, "register/register-success.html", locals())
 
