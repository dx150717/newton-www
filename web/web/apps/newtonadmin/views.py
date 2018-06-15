# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context, loader
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib.auth.decorators import user_passes_test

import decorators
from config import codes
from utils import http
from utils import security
from utils import exception
from . import forms

logger = logging.getLogger(__name__)

def show_login_view(request):
    form = forms.LoginForm()
    return render(request, "newtonadmin/login.html", locals())

def show_logout_view(request):
    logout(request)
    return redirect('/newtonadmin/login/')

@decorators.http_post_required
def post_login(request):
    try:
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "newtonadmin/login.html", locals())
        username = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password, is_staff=True)
        if not user or not user.is_staff:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_("Email or Password don't match")])
            return render(request, 'newtonadmin/login.html', locals())
        login(request, user)
        return redirect('/newtonadmin/')        
    except Exception, inst:
        logger.exception("fail to post login:%s" % str(inst))
        raise exception.SystemError500()
    
@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_index_view(request):
    return render(request, "newtonadmin/welcome.html", locals())

