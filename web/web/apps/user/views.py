# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.db.models import Sum
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
from tracker import models as tracker_models

logger = logging.getLogger(__name__)

@login_required
def show_user_index_view(request):
    """
    Show user index view.includes basic information, kyc information, tokenexchange information.
    """
    user = request.user
    user_form = forms.UserForm(instance=user)
    kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=user.id).first()
    if kycinfo:
        data = {}
        data = kycinfo.__dict__
        data['cellphone_group'] = {"country_code":kycinfo.country_code, "cellphone":kycinfo.cellphone}
        data['cellphone_of_emergency_contact'] ={"country_code":kycinfo.emergency_contact_country_code, "cellphone":kycinfo.emergency_contact_cellphone}
        base_form = token_exchange_forms.KYCBaseForm(initial=data)
        profile_form = token_exchange_forms.KYCProfileForm(initial=data)
        contribute_form = token_exchange_forms.ContributeForm(initial=data)
        emergency_form = token_exchange_forms.EmergencyForm(initial=data)
    kycaudit = tokenexchange_models.KYCAudit.objects.filter(user_id=user.id).last()
    items = tokenexchange_models.InvestInvite.objects.filter(user_id=user.id,status__gte=codes.TOKEN_EXCHANGE_STATUS_SEND_INVITE_NOTIFY_VALUE)
    for item in items:
        item.token_exchange_info = settings.FUND_CONFIG[item.phase_id]
    return render(request, "user/index.html", locals())

@login_required
def show_token_exchange_progress_view(request, phase_id):
    """
    query user who pass the kyc, than render his progress information.
    """
    try:
        user = request.user
        kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=user.id).first()
        kycaudit = tokenexchange_models.KYCAudit.objects.filter(user_id=user.id).first()
        item = tokenexchange_models.InvestInvite.objects.filter(user_id=user.id, phase_id=phase_id).first()
        btc_final_balance = 0
        ela_final_balance = 0
        if item:
            token_exchange_info = settings.FUND_CONFIG[item.phase_id]
            if item.receive_btc_address:
                btc_final_balance = tracker_models.AddressTransaction.objects.filter(address=item.receive_btc_address,address_type=codes.CurrencyType.BTC.value).aggregate(Sum('value'))
                btc_final_balance =  btc_final_balance.get("value__sum")
            if item.receive_ela_address:
                ela_final_balance = tracker_models.AddressTransaction.objects.filter(address=item.receive_ela_address,address_type=codes.CurrencyType.ELA.value).aggregate(Sum('value'))
                ela_final_balance = ela_final_balance.get("value__sum")
        if btc_final_balance and btc_final_balance != 0:
            item.btc_final_balance = btc_final_balance
        if ela_final_balance and ela_final_balance != 0:
            item.ela_final_balance = ela_final_balance
        return render(request, "user/token-exchange-progress.html", locals())
    except Exception,inst:
        logger.exception("error show progress %s" %str(inst))
        return http.HttpResponseServerError()
    