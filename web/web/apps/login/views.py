# -*- coding: utf-8 -*-
import logging
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from utils import http, security

logger = logging.getLogger(__name__)

def show_login_view(request):
    return render(request, 'login/index.html', locals())

def post_login(request):
    googleVerifyUrl = "https://www.google.com/recaptcha/api/siteverify"
    secretKey = "6LddrlUUAAAAAJDVSNQcnVsBJeDXSdToo_Gu2qvb"
    g_response = request.POST['g-recaptcha-response']
    post_data = {"secret":secretKey, "response":g_response}
    res = requests.post(googleVerifyUrl,post_data)
    '''
    {
        "success": true,
        "challenge_ts": "2018-04-26T07:30:26Z",
        "hostname": "localhost"
    }
    '''
    return redirect("/user/")
