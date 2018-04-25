# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from utils import http, security

logger = logging.getLogger(__name__)

def show_login_view(request):
    return render(request, 'login/index.html', locals())

def post_login(request):
    return redirect("/user/")
