# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User

import decorators
from utils import http
from config import codes
from . import forms
from . import services

logger = logging.getLogger(__name__)

def show_kyc_index_view(request):
    return render(request, "kyc/index.html", locals()) 

def show_join_kyc_view(request):
    form = forms.KYCInfoForm()
    return render(request, "kyc/submit.html", locals()) 

@login_required
@decorators.http_post_required
def post_kyc_information(request):
	try:
		# TODO twice submit kyc info need check.
		form = forms.KYCInfoForm(request.POST)
		if not form.is_valid():
			return render(request, "kyc/submit.html", locals()) 
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		email = request.user.email
		services.send_kyc_confirm_email(email, request)
		return redirect('/kyc/wait-audit/')
	except Exception, inst:
		logger.exception("fail to post kyc information:%s" % str(inst))
		return http.HttpResponseServerError()

def show_wait_audit_view(request):
    return render(request, "kyc/wait-audit.html", locals())
