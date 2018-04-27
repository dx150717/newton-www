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

from verification import service as register_email_service

from config import codes
from utils import http, security
from user import models as user_models
from . import forms

logger = logging.getLogger(__name__)

def show_register_view(request):
    form = forms.EmailForm()
    return render(request, 'register/index.html', locals())

def submit_email(request):
    try:
        if request.method == "POST":
            form = forms.EmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                # validate email is exist
                user = User.objects.filter(email=email)
                # validate user's status 
                if user:
                    return http.JsonErrorResponse(error_message=_('Email Has Exist!'))
                user = User.objects.create_user(email=email, username=security.generate_uuid())
                profile = user_models.UserProfile(user=user)
                profile.save()
                subject = _("NewtonProject Notifications: Please Confirm Subscription")
                targetUrl = settings.BASE_URL + "/subscribe/confirmed/?uuid=" + str(subscribed_email.uuid)
                template_html = "subscription/subscription-letter.html"
                to_email = subscribed_email.email_address
                email = form.cleaned_data['email']

    except Exception, inst:
        logger.error("file to submit email %s" %str(inst))
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
 
