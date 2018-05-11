# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.conf import settings
import pyotp

from utils import http
from config import codes
from . import forms
from . import models
import decorators
from tokenexchange import forms as token_exchange_forms
from tokenexchange import models as tokenexchange_models

logger = logging.getLogger(__name__)

@login_required
def show_user_index_view(request):
    user = request.user
    form = forms.UserForm(instance=user)
    kycinfo = tokenexchange_models.KYCInfo.objects.filter(user=user).first()
    kyc_form = token_exchange_forms.KYCInfoForm(instance=kycinfo)
    kycaudit = tokenexchange_models.KYCAudit.objects.filter(user=user).first()
    items = tokenexchange_models.InvestInvite.objects.filter(user=user,status__gte=codes.TOKEN_EXCHANGE_STATUS_SEND_INVITE_NOTIFY_VALUE)
    for item in items:
        item.token_exchange_info = settings.FUND_CONFIG[item.phase_id]
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

@login_required
def show_settings_view(request):
    profile = models.UserProfile.objects.filter(user=request.user).first()
    if not profile:
        return http.HttpResponseRedirect("/user/profile/")
    if profile.is_google_authenticator:
        toggle = "true"
    else:
        toggle = "false"
    return render(request, "user/settings.html", locals())

@login_required
def get_qrcode(request):
    gtoken = pyotp.random_base32()
    uri = pyotp.totp.TOTP(gtoken).provisioning_uri("newton",issuer_name="newton")
    return http.JsonSuccessResponse(data={"gtoken":gtoken,"uri":uri})

def post_settings(request):
    return render(request, "user/settings.html", locals())

def show_token_exchange_progress_view(request, phase_id):
    try:
        user = request.user
        kycinfo = tokenexchange_models.KYCInfo.objects.filter(user__id=user.id).first()
        kycaudit = tokenexchange_models.KYCAudit.objects.filter(user__id=user.id).first()
        item = tokenexchange_models.InvestInvite.objects.filter(user__id=user.id, phase_id=phase_id).first()
        btc_final_balance = 0
        ela_final_balance = 0
        if item:
            token_exchange_info = settings.FUND_CONFIG[item.phase_id]
            if item.receive_btc_address:
                btc_transaction = tokenexchange_models.AddressTransaction.objects.filter(address=item.receive_btc_address,address_type=codes.CurrencyType.BTC.value)
                if btc_transaction:
                    for t in btc_transaction:
                        btc_final_balance = btc_final_balance + float(t.value)
            if item.receive_ela_address:
                ela_transaction = tokenexchange_models.AddressTransaction.objects.filter(address=item.receive_ela_address,address_type=codes.CurrencyType.ELA.value)
                if ela_transaction:
                    for t in ela_transaction:
                        ela_final_balance = ela_final_balance + float(t.value)
        if btc_final_balance != 0:
            item.btc_final_balance = btc_final_balance
        if ela_final_balance != 0:
            item.ela_final_balance = ela_final_balance
        return render(request, "user/token-exchange-progress.html", locals())
    except Exception,inst:
        logger.exception("error show progress %s" %str(inst))
        return http.HttpResponseServerError()
    