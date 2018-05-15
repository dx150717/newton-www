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
        data['first_name'] = kycinfo.first_name
        data['last_name'] = kycinfo.last_name
        data['country'] = kycinfo.country
        data['id_number'] = kycinfo.id_number
        data['id_card'] = kycinfo.id_card
        data['cellphone_group'] = kycinfo.country_code + kycinfo.cellphone
        data['location'] = kycinfo.location
        data['how_to_contribute'] = kycinfo.how_to_contribute
        data['what_is_newton'] = kycinfo.what_is_newton
        data['emergency_contact_first_name'] = kycinfo.emergency_contact_first_name
        data['emergency_contact_last_name'] = kycinfo.emergency_contact_last_name
        data['cellphone_of_emergency_contact'] = kycinfo.emergency_contact_country_code + kycinfo.emergency_contact_cellphone
        data['relationships_with_emergency_contacts'] = kycinfo.relationships_with_emergency_contacts
        kyc_form = token_exchange_forms.KYCInfoForm(initial=data)
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
                btc_final_balance = tokenexchange_models.AddressTransaction.objects.filter(address=item.receive_btc_address,address_type=codes.CurrencyType.BTC.value).aggregate(Sum('value'))
            if item.receive_ela_address:
                ela_final_balance = tokenexchange_models.AddressTransaction.objects.filter(address=item.receive_ela_address,address_type=codes.CurrencyType.ELA.value).aggregate(Sum('value'))
        if btc_final_balance != 0:
            item.btc_final_balance = btc_final_balance
        if ela_final_balance != 0:
            item.ela_final_balance = ela_final_balance
        return render(request, "user/token-exchange-progress.html", locals())
    except Exception,inst:
        logger.exception("error show progress %s" %str(inst))
        return http.HttpResponseServerError()
    