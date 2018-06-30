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
from django.utils import translation

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

def apply_valid_required(func):
    """Check whether it is beyond the deadline of applying amount
    """
    def _decorator(request, *args, **kwargs):
        is_deadline_expired = tokenexchange_services.is_beyond_apply_deadline()
        if is_deadline_expired:
            return render(request, "tokenexchange/apply-end.html")
        return func(request, *args, **kwargs)
    return _decorator

@login_required
def show_tokenexchange_index_view(request):
    """
    Show kyc agreement.
    """
    return render(request, "tokenexchange/index.html", locals()) 

@login_required
@decorators.google_authenticator_required
def post_kyc_information(request, kyc_type):
    """
    Receive user's kyc information, and save them.
    """
    try:
        # check whether individual or orgnizition
        is_individual = True
        instance = tokenexchange_models.KYCInfo.objects.filter(user_id=request.user.id).first()
        # check user's kycinfo status
        if instance:
            if instance.status == codes.KYCStatus.CANDIDATE.value:
                return render(request, "tokenexchange/kyc-submit.html", locals())
            elif instance.status == codes.KYCStatus.PASS_KYC.value:
                return render(request, "tokenexchange/kyc-pass.html", locals())
            elif instance.status == codes.KYCStatus.DENY.value:
                return render(request, "tokenexchange/kyc-deny.html", locals())
        if kyc_type == codes.KYCType.ORGANIZATION.value:
            is_individual = False
        if request.method == 'POST':
            if kyc_type == codes.KYCType.INDIVIDUAL.value:
                # build a instance object
                if not instance:
                    instance = tokenexchange_models.KYCInfo()
                    instance.phase_id = settings.CURRENT_FUND_PHASE
                    instance.user_id = request.user.id
                # check whether individual post data is valid
                form = tokenexchange_forms.KYCIndividualForm(request.POST, request.FILES, instance=instance)
                if not form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
                # extract indivadual data
                instance = form.save(commit=False)
                country_code, cellphone = form.cleaned_data['cellphone_group']
                if form.cleaned_data['cellphone_of_emergency_contact']:
                    emergency_contact_country_code, emergency_contact_cellphone = form.cleaned_data['cellphone_of_emergency_contact']
                    instance.emergency_contact_country_code = emergency_contact_country_code
                    instance.emergency_contact_cellphone = emergency_contact_cellphone
                instance.country_code = country_code
                instance.cellphone = cellphone
                instance.kyc_type = kyc_type
                instance.status = codes.KYCStatus.CANDIDATE.value
                instance.save()
            else:
                # build a instance object
                if not instance:
                    instance = tokenexchange_models.KYCInfo()
                    instance.phase_id = settings.CURRENT_FUND_PHASE
                    instance.user_id = request.user.id
                # check whether organization post data is valid
                form = tokenexchange_forms.KYCOrganizationForm(request.POST, request.FILES, instance=instance)
                if not form.is_valid():
                    return render(request, "tokenexchange/submit.html", locals())
                # extract organization data
                instance = form.save(commit=False)
                country_code, cellphone = form.cleaned_data['cellphone_group']
                instance.country_code = country_code
                instance.cellphone = cellphone
                instance.kyc_type = kyc_type
                instance.status = codes.KYCStatus.CANDIDATE.value
                instance.save()
            return redirect('/tokenexchange/wait-audit/')
        else:
            is_chinese = False
            language_code = translation.get_language()
            if language_code.startswith('zh'):
                is_chinese = True
            country_form = tokenexchange_forms.CountryForm(instance=instance)
            organization_country_form = tokenexchange_forms.OrganizationCountryForm(instance=instance)
            emergency_country_form = tokenexchange_forms.EmergencyCountryForm(instance=instance)
            return render(request, "tokenexchange/submit.html", locals()) 
    except Exception, inst:
        logger.exception("fail to post kyc information:%s" % str(inst))
        raise exception.SystemError500()

@login_required
def show_wait_audit_view(request):
    return render(request, "tokenexchange/wait-audit.html", locals())

def show_invalid_link(request):
    return render(request, "tokenexchange/invalid-link.html", locals())
    
@login_required
@decorators.check_google_authenticator_session
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
        # check whether the fundraise process is expired
        is_deadline = False
        deadline_dt = datetime.datetime.strptime(token_exchange_info['end_date'], "%Y-%m-%d %H:%M")
        deadline_dt = deadline_dt.replace(tzinfo=utc)
        now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if now_time > deadline_dt:
            is_deadline = True
        # check whether the receive equal assign
        is_equal = True
        if invite_item.btc_final_balance != invite_item.assign_btc:
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
@apply_valid_required
@decorators.check_google_authenticator_session
def post_apply_amount(request, invite_id):
    """ Post the amount of apply
    """
    try:
        invite_id = int(invite_id)
        item = tokenexchange_models.InvestInvite.objects.filter(user_id=request.user.id, id=invite_id).first()
        if not item:
            raise exception.SystemError500()
        # get token exchange info
        token_exchange_info = settings.FUND_CONFIG[item.phase_id]
        min_btc = token_exchange_info['min_btc']
        #min_ela = token_exchange_info['min_ela']
        if request.method == 'POST':
            #if item.expect_btc or item.expect_ela:
            if item.expect_btc:
                message = unicode(_("You have applied."))
                return http.JsonErrorResponse(error_message=message)
            form = tokenexchange_forms.ApplyAmountForm(request.POST)
            if not form.is_valid():
                message = unicode(_("BTC is required."))
                return http.JsonErrorResponse(error_message=message)
            else:
                expect_btc = form.cleaned_data['expect_btc']
                #expect_ela = form.cleaned_data['expect_ela']
                #if not expect_btc and not expect_ela:
                if not expect_btc:
                    return http.JsonErrorResponse(error_message=unicode(_('BTC is required.')))
                elif expect_btc and expect_btc < min_btc:
                    message = unicode(_('The quantity of BTC must be equal or more than %s.')) % (min_btc)
                    return http.JsonErrorResponse(error_message=message)
                #elif expect_ela and expect_ela < min_ela:
                #    message = unicode(_('The quantity of ELA must be equal or more than %s.')) % (min_ela)
                #    return http.JsonErrorResponse(error_message=message)
                item.expect_btc = expect_btc
                #item.expect_ela = expect_ela
                item.status = codes.TokenExchangeStatus.APPLY_AMOUNT.value
                item.save()
                return http.JsonSuccessResponse({'redirect_url': '/tokenexchange/invite/%s/success/' % invite_id})
        else:
            form = tokenexchange_forms.ApplyAmountForm()
        #if item.expect_btc or item.expect_ela:
        if item.expect_btc:
            return render(request, "tokenexchange/invalid-link.html")
        return render(request, "tokenexchange/apply-amount.html", locals())
    except Exception, inst:
        logger.exception("fail to post the apply amount:%s" % str(inst))
        raise exception.SystemError500()

@login_required
@apply_valid_required
@decorators.check_google_authenticator_session
def show_apply_success(request, invite_id):
    """Show the page of apply success
    """
    try:
        return render(request, "tokenexchange/apply-success.html", locals())
    except Exception, inst:
        logger.exception("fail to show the apply success page:%s" % str(inst))
        raise exception.SystemError500()
