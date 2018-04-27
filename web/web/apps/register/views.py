# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.shortcuts import render,redirect
from django.core.validators import validate_email
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.template import Template, Context, loader

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
            return http.JsonErrorResponse(error_message=_("Email had Register!"))
        is_send_success = services.send_register_validate_email(email)
        if not is_send_success:
            return http.HttpResponseServerError()
        else:
            return http.HttpResponseRedirect('/register/post-success/')
    except Exception, inst:
        print(str(inst))
        logger.exception('fail to submit email: %s' % str(inst))
        return http.HttpResponseServerError()

def show_post_email_success_view(request):
    return render(request, 'register/post-success.html', locals())

def show_post_email_fail_view(request):
    return render(request, 'register/post-fail.html', locals())

def verify_email_link(request):
    return http.HttpResponseRedirect('/register/password/')

def show_password_view(request):
    return render(request, 'register/password.html', locals())

def submit_password(request):
    return http.HttpResponseRedirect('/user/')
 
