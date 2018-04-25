# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User

from utils import http
from config import codes

logger = logging.getLogger(__name__)

def show_kyc_index_view(request):
    return render(request, "kyc/index.html", locals()) 

def show_join_kyc_view(request):
    return render(request, "kyc/submit.html", locals()) 

def post_kyc_information(request):
    return redirect('/kyc/wait-audit/')

def show_wait_audit_view(request):
    return render(request, "kyc/wait-audit.html", locals())
