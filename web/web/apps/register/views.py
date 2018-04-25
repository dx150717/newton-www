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

from config import codes
from utils import http, security
from user import models as user_models
import forms

logger = logging.getLogger(__name__)

def show_register_view(request):
    return render(request, 'register/index.html', locals())

def submit_email(request):
    return http.HttpResponseRedirect('/register/post-success/')

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
 
