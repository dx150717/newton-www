# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.conf import settings

import decorators
from utils import http
from config import codes
from . import forms
from . import services
from . import models as tokensale_models

logger = logging.getLogger(__name__)

@login_required
def show_tokensale_index_view(request):
    return render(request, "tokensale/index.html", locals()) 

@login_required
def show_join_tokensale_view(request):
    instance = tokensale_models.KYCInfo.objects.filter(user=request.user, phase_id=settings.CURRENT_FUND_PHASE).first()
    form = forms.KYCInfoForm(instance=instance)
    return render(request, "tokensale/submit.html", locals()) 

@login_required
@decorators.http_post_required
def post_kyc_information(request):
    try:
        # TODO twice submit tokensale info need check.
        form = forms.KYCInfoForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "tokensale/submit.html", locals())
        # check whether user is submit kyc info
        instance = tokensale_models.KYCInfo.objects.filter(user=request.user, phase_id=settings.CURRENT_FUND_PHASE).first()
        instance = form.save(commit=False)
        instance.phase_id = settings.CURRENT_FUND_PHASE
        instance.user = request.user
        instance.save()
        email = request.user.email
        services.send_kyc_confirm_email(email, request)
        return redirect('/tokensale/wait-audit/')
    except Exception, inst:
        logger.exception("fail to post kyc information:%s" % str(inst))
        return http.HttpResponseServerError()

@login_required
def show_wait_audit_view(request):
    return render(request, "tokensale/wait-audit.html", locals())

@login_required
def show_receive_address_view(request, username):
    try:
        user = User.objects.get(username=username)
        item = tokensale_models.KYCInfo.objects.get(phase_id=settings.CURRENT_FUND_PHASE, user=user)
        return render(request, "tokensale/receive-address.html", locals())
    except Exception, inst:
        logger.exception("fail to show receive address:%s" % str(inst))
        return http.HttpResponseServerError()
 
