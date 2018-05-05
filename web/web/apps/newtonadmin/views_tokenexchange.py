# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from utils import http
from config import codes
from tokenexchange import models as tokenexchange_models
from . import forms_tokenexchange
from . import services_tokenexchange

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_id_list_view(request):
    """Show the candiate ID list
    
    """
    try:
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.CANDIDATE.value)
        return render(request, "newtonadmin/id-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show id list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_pass_id_list_view(request):
    """Show the pass ID list
    
    """
    try:
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.PASS_KYC.value)
        return render(request, "newtonadmin/pass-id-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show id list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_id(request):
    """Confirm whether ID is valid
    
    """
    try:
        form = forms_tokenexchange.ConfirmKYCForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        pass_tokenexchange = int(form.cleaned_data['pass_kyc'])
        level = int(form.cleaned_data['level'])
        item = tokenexchange_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CANDIDATE.value)
        if pass_tokenexchange:
            item.status = codes.KYCStatus.PASS_KYC.value
            item.level = level
        else:
            item.status = codes.KYCStatus.REJECT.value
        item.save()
        # send the kyc pass notify
        services_tokenexchange.send_kyc_pass_notify(item, request)
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to confirm id:%s" % str(inst))
        return http.JsonErrorResponse()        

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_invite_view(request, phase_id):
    """Show the investor list which is waiting for invite
    
    """
    try:
        phase_id = int(phase_id)
        s1 = set(tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.PASS_KYC.value).values_list('user', flat=True))
        s2 = set(tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id).values_list('user', flat=True))
        d = s1.difference(s2)
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.PASS_KYC.value, user__id__in=d)
        return render(request, "newtonadmin/te-waiting-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show the te wait list:%s" % str(inst))
        return http.HttpResponseServerError()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def post_invite(request, phase_id):
    try:
        form = forms_tokenexchange.PostInviteForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user__id=user_id).first()
        if not invite:
            invite = tokenexchange_models.InvestInvite()
            invite.user_id = user_id
            invite.phase_id = int(phase_id)
        invite.status = codes.TokenExchangeStatus.INVITE.value
        invite.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post invite:%s" % str(inst))
        return http.JsonErrorResponse()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_completed_invite_view(request, phase_id):
    """Show the investor list which is completed for invite
    
    """
    try:
        phase_id = int(phase_id)
        items = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id).order_by('-created_at')
        return render(request, "newtonadmin/te-completed-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show the te completed list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def send_invite_email(request, phase_id):
    try:
        form = forms_tokenexchange.PostInviteForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        phase_id = int(phase_id)
        invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user__id=user_id).first()
        if not invite:
            return http.JsonErrorResponse()
        if services_tokenexchange.send_apply_amount_notify(invite, request):
            invite.status = codes.TokenExchangeStatus.SEND_INVITE_NOTIFY.value
            invite.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to send the invite email:%s" % str(inst))
        return http.JsonErrorResponse()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_amount_list_view(request):
    """Show the investor list which we pass KYC
    
    """
    try:
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.TokenExchangeStatus.APPLY_AMOUNT.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/amount-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show amount list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_amount(request):
    """Show the investor list which we don't set the invest amount
    
    """
    try:
        form = forms_tokenexchange.AmountForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        min_btc_limit = int(form.cleaned_data['min_btc_limit'])
        max_btc_limit = int(form.cleaned_data['max_btc_limit'])
        min_ela_limit = int(form.cleaned_data['min_ela_limit'])
        max_ela_limit = int(form.cleaned_data['max_ela_limit'])
        # Query the available address
        btc_address = services_tokenexchange.allocate_btc_address()
        ela_address = services_tokenexchange.allocate_ela_address()
        if not btc_address or not ela_address:
            return http.JsonErrorResponse()
        # save status
        item = tokenexchange_models.KYCInfo.objects.get(user__id=user_id, status=codes.TokenExchangeStatus.APPLY_AMOUNT.value, phase_id=settings.CURRENT_FUND_PHASE)
        item.status = codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value
        item.min_btc_limit = min_btc_limit
        item.max_btc_limit = max_btc_limit
        item.min_ela_limit = min_ela_limit
        item.max_ela_limit = max_ela_limit
        item.receive_btc_address = btc_address
        item.receive_ela_address = ela_address
        item.save()
        services_tokenexchange.send_confirm_distribution_notify(item, request)
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to confirm amount:%s" % str(inst))
        return http.JsonErrorResponse()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_email_list_view(request):
    """Show the investor list which we don't send the final email to
    
    """
    try:
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.TokenExchangeStatus.CONFIRM_DISTRIBUTION.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/email-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show email list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_email(request):
    """Determine whether send email to investor
    
    """
    try:
        user_id = int(request.POST['user_id'])
        item = tokenexchange_models.KYCInfo.objects.filter(user__id=user_id, status=codes.TokenExchangeStatus.CONFIRM_DISTRIBUTION.value, phase_id=settings.CURRENT_FUND_PHASE).first()
        if not item:
            logger.error("item is not found.")
            return http.JsonErrorResponse()
        if services_tokenexchange.send_distribution_letter(item.user, request):
            item.status = codes.TokenExchangeStatus.SEND_TRANSFER_NOTIFY.value
            item.save()
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse()
    except Exception, inst:
        logger.exception("fail to confirm email:%s" % str(inst))
        return http.JsonErrorResponse()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_sent_list_view(request):
    """Show the investor list which we have already sent the final email to
    
    """
    try:
        items = tokenexchange_models.KYCInfo.objects.filter(status=codes.TokenExchangeStatus.SEND_TRANSFER_NOTIFY.value, phase_id=settings.CURRENT_FUND_PHASE).order_by('-created_at')
        return render(request, "newtonadmin/sent-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show sent list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_receive_list_view(request):
    """Show the investor list who send money to newton foundation
    
    """
    try:
        items = tokenexchange_models.AddressTransaction.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).order_by('-created_at')
        return render(request, "newtonadmin/receive-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show receive list:%s" % str(inst))
        return http.HttpResponseServerError()    

