# -*- coding: utf-8 -*-
import logging
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms.forms import NON_FIELD_ERRORS

import decorators
from utils import http
from config import codes
from . import forms
from . import services
from . import models as tokenexchange_models

logger = logging.getLogger(__name__)

def exchange_valid_required(func):
    """
    """
    def _decorator(request, *args, **kwargs):
        now = datetime.datetime.now()
        if now < settings.FUND_START_DATE:
            return redirect('/tokenexchange/pending/')
        elif now > settings.FUND_END_DATE:
            return redirect('/tokenexchange/end/')
        else:
            return func(request, *args, **kwargs)
    return _decorator

#@exchange_valid_required
@login_required
def show_tokenexchange_index_view(request):
    """
    Show kyc agreement.
    """
    return render(request, "tokenexchange/index.html", locals()) 

#@exchange_valid_required
@login_required
def post_kyc_information(request):
    """
    Receive user's kyc information, and save them.
    """
    try:
        if request.method == 'POST':
            # check whether user is submit kyc info
            instance = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
            
            if not instance:
                instance = tokenexchange_models.KYCInfo()

            base_form = forms.KYCBaseForm(request.POST, request.FILES, instance=instance)
            profile_form = forms.KYCProfileForm(request.POST, request.FILES, instance=instance)
            contribute_form = forms.ContributeForm(request.POST, request.FILES, instance=instance)
            emergency_form = forms.EmergencyForm(request.POST, request.FILES, instance=instance)

            if instance and instance.status == codes.KYCStatus.PASS_KYC.value:
                base_form._errors[NON_FIELD_ERRORS] = base_form.error_class([_('You had submited kyc info')])
                return render(request, "tokenexchange/submit.html", locals())
            

            if not base_form.is_valid():
                return render(request, "tokenexchange/submit.html", locals())
            if not profile_form.is_valid():
                return render(request, "tokenexchange/submit.html", locals())  
            if not contribute_form.is_valid():
                return render(request, "tokenexchange/submit.html", locals())
            if not emergency_form.is_valid():
                return render(request, "tokenexchange/submit.html", locals())

            instance.user_id = request.user.id
            instance = base_form.save(commit=True)
            instance = profile_form.save(commit=True)
            instance = contribute_form.save(commit=True)
            instance = emergency_form.save(commit=True)

            is_etablish_node = request.POST.get('is_etablish_node')
            which_node_establish = request.POST.get('which_node_establish')
            establish_node_plan = request.POST.get('establish_node_plan')
            if establish_node_plan and len(establish_node_plan) < 10240:
                instance.establish_node_plan = establish_node_plan
            instance.is_etablish_node = is_etablish_node
            instance.which_node_establish = which_node_establish
            country_code, cellphone = base_form.cleaned_data['cellphone_group']
            instance.country_code = country_code
            instance.cellphone = cellphone
            emergency_contact_country_code, emergency_contact_cellphone = emergency_form.cleaned_data['cellphone_of_emergency_contact']
            instance.emergency_contact_country_code = emergency_contact_country_code
            instance.emergency_contact_cellphone = emergency_contact_cellphone
            instance.phase_id = settings.CURRENT_FUND_PHASE
            instance.status = codes.KYCStatus.CANDIDATE.value
            instance.save()
                        
            instance = base_form.save(commit=True)
            instance = profile_form.save(commit=True)
            instance = contribute_form.save(commit=True)
            instance = emergency_form.save(commit=True)

            return redirect('/tokenexchange/wait-audit/')
        else:
            instance = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
            base_form = forms.KYCBaseForm(instance=instance)
            profile_form = forms.KYCProfileForm(instance=instance)
            contribute_form = forms.ContributeForm(instance=instance)
            emergency_form = forms.EmergencyForm(instance=instance)
            return render(request, "tokenexchange/submit.html", locals()) 
    except Exception, inst:
        logger.exception("fail to post kyc information:%s" % str(inst))
        return http.HttpResponseServerError()

#@exchange_valid_required
@login_required
def show_wait_audit_view(request):
    return render(request, "tokenexchange/wait-audit.html", locals())

def show_invalid_link(request):
    return render(request, "tokenexchange/invalid-link.html", locals())
    
@login_required
def show_receive_address_view(request, username):
    try:
        user = User.objects.get(username=username)
        item = tokenexchange_models.KYCInfo.objects.filter(phase_id=settings.CURRENT_FUND_PHASE, user=user).first()
        return render(request, "tokenexchange/receive-address.html", locals())
    except Exception, inst:
        logger.exception("fail to show receive address:%s" % str(inst))
        return http.HttpResponseServerError()
 
def show_pending_view(request):
    now = datetime.datetime.now()
    delta_time = settings.FUND_START_DATE - now
    delta_time = delta_time.total_seconds()
    return render(request, "tokenexchange/pending.html", locals())

def show_end_view(request):
    return render(request, "tokenexchange/end.html", locals())

@login_required
def post_apply_amount(request, invite_id):
    """ Post the amount of apply
    """
    try:
        invite_id = int(invite_id)
        item = tokenexchange_models.InvestInvite.objects.filter(user_id=request.user.id, id=invite_id).first()
        if not item:
            return http.HttpResponseServerError()
        if item.expect_btc or item.expect_ela:
            return render(request, "tokenexchange/invalid-link.html")
        if request.method == 'POST':
            form = forms.ApplyAmountForm(request.POST)
            if form.is_valid():
                item.expect_btc = form.cleaned_data['expect_btc']
                item.expect_ela = form.cleaned_data['expect_ela']
                if not item.expect_btc and not item.expect_ela:
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['You must fill in at least one.'])
                    return render(request, "tokenexchange/apply-amount.html", locals())
                item.status = codes.TokenExchangeStatus.APPLY_AMOUNT.value
                item.save()
                token_exchange_info = settings.FUND_CONFIG[item.phase_id]
                return render(request, "tokenexchange/apply-success.html", locals())
        else:
            token_exchange_info = settings.FUND_CONFIG[item.phase_id]
            form = forms.ApplyAmountForm()
        return render(request, "tokenexchange/apply-amount.html", locals())
    except Exception, inst:
        logger.exception("fail to post the apply amount:%s" % str(inst))
        return http.HttpResponseServerError()
