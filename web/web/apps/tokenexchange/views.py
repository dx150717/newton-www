# -*- coding: utf-8 -*-
import logging
import datetime
import time

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
from utils import exception
from config import codes
from . import forms as tokenexchange_forms
from . import services as tokenexchange_services
from . import models as tokenexchange_models
from tracker import models as tracker_models
from django.db.models import Sum
from django.utils.timezone import utc

logger = logging.getLogger(__name__)

def kyc_valid_required(func):
    """Check whether kyc is expired
    """
    def _decorator(request, *args, **kwargs):
        is_deadline_expired = tokenexchange_services.is_beyond_kyc_deadline()
        if is_deadline_expired:
            return render(request, "tokenexchange/kyc-end.html")
        return func(request, *args, **kwargs)
    return _decorator

@login_required
@kyc_valid_required
def show_tokenexchange_index_view(request):
    """
    Show kyc agreement.
    """
    return render(request, "tokenexchange/index.html", locals()) 

@login_required
@kyc_valid_required
def post_kyc_information(request, kyc_type):
    """
    Receive user's kyc information, and save them.
    """
    try:
        # check whether individual or orgnizition
        is_individual = True
        if kyc_type == codes.KYCType.ORGANIZATION.value:
            is_individual = False
        if request.method == 'POST':
            # check user's kycinfo status
            kycinfo_item = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
            if kycinfo_item:
                if kycinfo_item.status == codes.KYCStatus.DENY.value:
                    return render(request, "tokenexchange/kyc-deny.html", locals())
            # check whether user is submit kyc info
            instance = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
            if not instance:
                instance = tokenexchange_models.KYCInfo()
            instance.kyc_type = kyc_type
            instance.phase_id = settings.CURRENT_FUND_PHASE
            # chekc whether user has pass kyc
            if instance and instance.status == codes.KYCStatus.PASS_KYC.value:
                base_form._errors[NON_FIELD_ERRORS] = base_form.error_class([_('You had submited kyc info')])
                return render(request, "tokenexchange/submit.html", locals())
            # check whether post data is valid
            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                base_form = tokenexchange_forms.KYCBaseForm(request.POST, request.FILES, instance=instance)
                profile_form = tokenexchange_forms.KYCProfileForm(request.POST, request.FILES, instance=instance)
                emergency_form = tokenexchange_forms.EmergencyForm(request.POST, request.FILES, instance=instance)
                if not base_form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
                if not profile_form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
                if not emergency_form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
            else:
                organization_base_form = tokenexchange_forms.OrganizationBaseForm(request.POST, request.FILES, instance=instance)
                organization_profile_form = tokenexchange_forms.OrganizationProfileForm(request.POST, request.FILES, instance=instance)
                if not organization_base_form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
                if not organization_profile_form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
            contribute_form = tokenexchange_forms.ContributeForm(request.POST, request.FILES, instance=instance)
            if not contribute_form.is_valid():
                return render(request, "tokenexchange/submit.html", locals())
            # insert data into sql
            instance.user_id = request.user.id
            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                instance = base_form.save(commit=True)
                instance = profile_form.save(commit=True)
                instance = emergency_form.save(commit=True)
            else:
                instance = organization_base_form.save(commit=True)
                instance = organization_profile_form.save(commit=True)
            instance = contribute_form.save(commit=True)

            is_etablish_node = request.POST.get('is_etablish_node')
            which_node_establish = request.POST.get('which_node_establish')
            establish_node_plan = request.POST.get('establish_node_plan')
            if establish_node_plan and len(establish_node_plan) < 10240:
                instance.establish_node_plan = establish_node_plan
            instance.is_etablish_node = is_etablish_node
            instance.which_node_establish = which_node_establish
            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                country_code, cellphone = base_form.cleaned_data['cellphone_group']
            else:
                country_code, cellphone = organization_base_form.cleaned_data['cellphone_group']
            instance.country_code = country_code
            instance.cellphone = cellphone
            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                emergency_contact_country_code, emergency_contact_cellphone = emergency_form.cleaned_data['cellphone_of_emergency_contact']
                instance.emergency_contact_country_code = emergency_contact_country_code
                instance.emergency_contact_cellphone = emergency_contact_cellphone
            instance.status = codes.KYCStatus.CANDIDATE.value
            instance.save()

            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                instance = base_form.save(commit=True)
                instance = profile_form.save(commit=True)
                instance = emergency_form.save(commit=True)
            else:
                instance = organization_base_form.save(commit=True)
                instance = organization_profile_form.save(commit=True)
            instance = contribute_form.save(commit=True)

            return redirect('/tokenexchange/wait-audit/')
        else:
            instance = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
            base_form = tokenexchange_forms.KYCBaseForm(instance=instance)
            profile_form = tokenexchange_forms.KYCProfileForm(instance=instance)
            contribute_form = tokenexchange_forms.ContributeForm(instance=instance)
            emergency_form = tokenexchange_forms.EmergencyForm(instance=instance)
            organization_base_form = tokenexchange_forms.OrganizationBaseForm(instance=instance)
            organization_profile_form = tokenexchange_forms.OrganizationProfileForm(instance=instance)
            return render(request, "tokenexchange/submit.html", locals()) 
    except Exception, inst:
        logger.exception("fail to post kyc information:%s" % str(inst))
        raise exception.SystemError500()

@login_required
@kyc_valid_required
def show_wait_audit_view(request):
    return render(request, "tokenexchange/wait-audit.html", locals())

def show_invalid_link(request):
    return render(request, "tokenexchange/invalid-link.html", locals())
    
@login_required
@kyc_valid_required
def show_receive_address_view(request, invite_id):
    """Show the receive address
    """
    try:
        # handle the input parameter
        invite_id = int(invite_id)
        user = request.user
        # check whether the given invite_id is valid
        invite_item = tokenexchange_models.InvestInvite.objects.filter(user_id=user.id, id=invite_id).first()
        if not invite_item:
            return http.HttpResponseNotFound()
        if invite_item.status == codes.TokenExchangeStatus.SEND_INVITE_NOTIFY.value:
            return http.HttpResponseRedirect("/tokenexchange/invite/" + str(invite_item.id) + "/post/")
        # query data
        invite_item.btc_final_balance = 0
        invite_item.btc_transfer_list = []
        invite_item.ela_final_balance = 0
        invite_item.ela_transfer_list = []
        token_exchange_info = settings.FUND_CONFIG[invite_item.phase_id]
        # btc section
        if invite_item.receive_btc_address:
            btc_final_balance = tracker_models.AddressTransaction.objects.filter(address=invite_item.receive_btc_address,address_type=codes.CurrencyType.BTC.value).aggregate(Sum('value'))
            btc_final_balance =  btc_final_balance.get("value__sum", 0)
            btc_transfer_list = tracker_models.AddressTransaction.objects.filter(address=invite_item.receive_btc_address,address_type=codes.CurrencyType.BTC.value)
            if btc_final_balance > 0:
                invite_item.btc_final_balance = btc_final_balance
                invite_item.btc_transfer_list = btc_transfer_list
        # ela section
        if invite_item.receive_ela_address:
            ela_final_balance = tracker_models.AddressTransaction.objects.filter(address=invite_item.receive_ela_address,address_type=codes.CurrencyType.ELA.value).aggregate(Sum('value'))
            ela_final_balance = ela_final_balance.get("value__sum", 0)
            ela_transfer_list = tracker_models.AddressTransaction.objects.filter(address=invite_item.receive_ela_address,address_type=codes.CurrencyType.ELA.value)
            if ela_final_balance > 0:
                invite_item.ela_final_balance = ela_final_balance
                invite_item.ela_transfer_list = ela_transfer_list
        # check whether the fundraise process is expired
        is_deadline = False
        deadline_time = time.strptime(token_exchange_info['end_date'], "%Y-%m-%d")
        dead_time = datetime.datetime(*deadline_time[:6]).replace(tzinfo=utc)
        now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if now_time > dead_time:
            is_deadline = True
        # check whether the receive equal assign
        is_equal = True
        if invite_item.btc_final_balance != invite_item.assign_btc or invite_item.ela_final_balance != invite_item.assign_ela:
            is_equal = False
        return render(request, "tokenexchange/token-exchange-receive-address.html", locals())
    except Exception,inst:
        logger.exception("fail to  show receive address: %s" % str(inst))
        raise exception.SystemError500()
 
def show_pending_view(request):
    now = datetime.datetime.now()
    delta_time = settings.FUND_START_DATE - now
    delta_time = delta_time.total_seconds()
    return render(request, "tokenexchange/pending.html", locals())

def show_end_view(request):
    return render(request, "tokenexchange/end.html", locals())

@login_required
@kyc_valid_required
def post_apply_amount(request, invite_id):
    """ Post the amount of apply
    """
    try:
        invite_id = int(invite_id)
        item = tokenexchange_models.InvestInvite.objects.filter(user_id=request.user.id, id=invite_id).first()
        if not item:
            raise exception.SystemError500()
        if item.expect_btc or item.expect_ela:
            return render(request, "tokenexchange/invalid-link.html")
        if request.method == 'POST':
            form = tokenexchange_forms.ApplyAmountForm(request.POST)
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
            form = tokenexchange_forms.ApplyAmountForm()
        return render(request, "tokenexchange/apply-amount.html", locals())
    except Exception, inst:
        logger.exception("fail to post the apply amount:%s" % str(inst))
        raise exception.SystemError500()
