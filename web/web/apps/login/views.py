# -*- coding: utf-8 -*-
import logging
import requests
import json
import urlparse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.timezone import utc
from django.forms.forms import NON_FIELD_ERRORS

import decorators
from utils import http
from utils import security
from . import forms

logger = logging.getLogger(__name__)

def show_login_view(request):
    form = forms.LoginForm()
    next = request.GET.get('next')
    return render(request, 'login/index.html', locals())

@decorators.http_post_required
def post_login(request):
    try:
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'login/index.html', locals())
        # g_recaptcha_response = request.POST.get('g-recaptcha-response')
        # post_data = {"secret":settings.GOOGLE_SECRET_KEY, "response":g_recaptcha_response}
        # res = requests.post(settings.GOOGLE_VERIFICATION_URL, post_data)
        # res = json.loads(res.text)
        # if not res['success']:
        #     form._errors[NON_FIELD_ERRORS] = form.error_class([_("No captcha")])
        #     return render(request, 'login/index.html', locals())
        # start authenticate
        username = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user or user.is_staff:
            form._errors[NON_FIELD_ERRORS] = form.error_class([_("Email or Password don't match")])
            return render(request, 'login/index.html', locals())
        login(request, user)
        next = request.POST.get('next')
        if next:
            result = urlparse.urlparse(next)
            if not result.netloc:
                return redirect(next)
        return redirect('/user/')
    except Exception, inst:
        logger.exception("fail to post login:%s" % str(inst))
        return http.HttpResponseServerError()
