# -*- coding: utf-8 -*-
import logging
import time
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.db.models import Sum
from django.contrib.auth.models import User
from django.conf import settings
import pyotp
from django_countries.data import COUNTRIES
from django.utils.timezone import utc

from utils import http
from utils import convert
from utils import exception
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
        if data['id_type']:
            data['id_type'] = convert.get_value_from_choice(data['id_type'], tokenexchange_models.ID_CHOICES)
        if data['is_establish_node']:
            data['is_establish_node'] = convert.get_value_from_choice(data['is_establish_node'], tokenexchange_models.ESTABLISH_CHOICE)
        if data['which_node_establish']:
            data['which_node_establish'] = convert.get_value_from_choice(data['which_node_establish'], tokenexchange_models.NODE_CHOICE)
        data['country'] = COUNTRIES[data['country']]
        data['emergency_country'] = COUNTRIES[data['emergency_country']]
        base_form = token_exchange_forms.KYCBaseForm(initial=data)
        profile_form = token_exchange_forms.KYCProfileForm(initial=data)
        contribute_form = token_exchange_forms.ContributeForm(initial=data)
        emergency_form = token_exchange_forms.EmergencyForm(initial=data)
    kycaudit = tokenexchange_models.KYCAudit.objects.filter(user_id=user.id).last()
    items = tokenexchange_models.InvestInvite.objects.filter(user_id=user.id,status__gte=codes.TOKEN_EXCHANGE_STATUS_SEND_INVITE_NOTIFY_VALUE)
    for item in items:
        item.token_exchange_info = settings.FUND_CONFIG[item.phase_id]
    return render(request, "user/index.html", locals())

    
