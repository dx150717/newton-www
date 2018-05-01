# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User

from utils import http
from config import codes
from . import forms
from . import models
import decorators

logger = logging.getLogger(__name__)

@login_required
def show_user_index_view(request):
    id = request.user.id
    user = User.objects.filter(id=id).first()
    if not user:
        return http.HttpResponseRedirect("/login/")
    profile = models.UserProfile.objects.filter(user=user).first()
    form = forms.UserProfileForm(instance=profile)
    return render(request, "user/index.html", locals()) 

@login_required
@decorators.http_get_required
def show_user_profile_view(request):
    profile = models.UserProfile.objects.filter(user=request.user).first()
    form = forms.UserProfileForm(instance=profile)
    return render(request, "user/profile.html", locals())

@login_required
@decorators.http_post_required
def post_profile(request):
    try:
        profile = models.UserProfile.objects.filter(user=request.user).first()
        form = forms.UserProfileForm(request.POST,instance=profile)
        if not form.is_valid():
            return render(request, "user/profile.html", locals())
        form.save()
        cellphone_group = form.cleaned_data['cellphone_group']
        country_code = cellphone_group[0]
        cellphone = cellphone_group[1]
        profile.country_code = country_code
        profile.cellphone = cellphone
        profile.save()
        return http.HttpResponseRedirect("/user/")
    except Exception, inst:
        logger.exception("fail to post profile %s" %str(inst))
        return http.HttpResponseServerError()

def show_settings_view(request):
    return render(request, "user/settings.html", locals())

def post_settings(request):
    return render(request, "user/settings.html", locals())