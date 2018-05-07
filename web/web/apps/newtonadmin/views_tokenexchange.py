# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.models import User

from utils import http
from config import codes
from tokenexchange import models as tokenexchange_models
from newtonadmin import models as newtonadmin_models
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
        comment = form.cleaned_data['comment']
        item = tokenexchange_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CANDIDATE.value)
        if pass_tokenexchange:
            item.status = codes.KYCStatus.PASS_KYC.value
            item.level = level
            action_id = codes.AdminActionType.PASS_KYC.value
            is_pass = True
        else:
            item.status = codes.KYCStatus.REJECT.value
            action_id = codes.AdminActionType.REJECT_KYC.value
            is_pass = False
        item.save()
        target_user = User.objects.filter(id=user_id).first()
        # add kyc audit
        kyc_audit = tokenexchange_models.KYCAudit(user=target_user,is_pass=is_pass,comment=comment)
        kyc_audit.save()
        # add audit log
        audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id,comment=comment)
        audit_log.save()
        # send the kyc pass notify
        item.kyc_audit = kyc_audit
        services_tokenexchange.send_kycinfo_notify(item, request)
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
        items = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, status__in=[codes.TokenExchangeStatus.INVITE.value, codes.TokenExchangeStatus.SEND_INVITE_NOTIFY.value]).order_by('-created_at')
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
def show_amount_list_view(request, phase_id):
    """Show the investor list which we pass KYC
    
    """
    try:
        phase_id = int(phase_id)
        items = tokenexchange_models.InvestInvite.objects.filter(status=codes.TokenExchangeStatus.APPLY_AMOUNT.value, phase_id=phase_id)
        form = forms_tokenexchange.AmountForm()
        return render(request, "newtonadmin/amount-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show the amount list:%s" % str(inst))
        return http.HttpResponseServerError()

def show_completed_amount_list_view(request, phase_id):
    """Show the investor list which are assigned the invest amount
    
    """
    try:
        is_completed = True
        phase_id = int(phase_id)
        items = tokenexchange_models.InvestInvite.objects.filter(status=codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value, phase_id=phase_id)
        form = forms_tokenexchange.AmountForm()
        return render(request, "newtonadmin/amount-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show the completed amount list:%s" % str(inst))
        return http.HttpResponseServerError()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def post_amount(request, phase_id):
    """submit the distribution amount
    
    """
    try:
        form = forms_tokenexchange.AmountForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        phase_id = int(phase_id)
        user_id = int(form.cleaned_data['user_id'])
        assign_btc = int(form.cleaned_data['assign_btc'])
        assign_ela = int(form.cleaned_data['assign_ela'])
        # Query the available address
        if assign_btc != 0:
            btc_address = services_tokenexchange.allocate_btc_address()
        else:
            btc_address = None
        if assign_ela == 0:
            ela_address = None
        else:
            ela_address = services_tokenexchange.allocate_ela_address()
        if not btc_address and not ela_address:
            return http.JsonErrorResponse()
        # save status
        item = tokenexchange_models.InvestInvite.objects.get(user__id=user_id, status=codes.TokenExchangeStatus.APPLY_AMOUNT.value, phase_id=phase_id)
        item.status = codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value
        item.assign_ela = assign_ela
        item.assign_btc = assign_btc
        item.receive_btc_address = btc_address
        item.receive_ela_address = ela_address
        item.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post amount:%s" % str(inst))
        return http.JsonErrorResponse()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_receive_list_view(request, phase_id):
    """Show the investor list who send money to newton foundation
    
    """
    try:
        phase_id = int(phase_id)
        items = tokenexchange_models.AddressTransaction.objects.filter(phase_id=phase_id).order_by('-created_at')
        return render(request, "newtonadmin/receive-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show receive list:%s" % str(inst))
        return http.HttpResponseServerError()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def send_receive_email(request, phase_id):
    """Send email to investor for notifing them that we have recevied coin.
    """
    try:
        phase_id = int(phase_id)
        address = request.POST['address']
        item = tokenexchange_models.AddressTransaction.objects.filter(phase_id=phase_id, address=address).first()
        invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user__id=item.user_id).first()
        if services_tokenexchange.send_receive_confirm_notify(request, item):
            invite.status = codes.TokenExchangeStatus.SEND_RECEIVE_AMOUNT_NOTIFY.value
            invite.save()
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="send Error")
    except Exception, inst:
        logger.exception("fail to post email to investor:%s" % str(inst))
        return http.JsonErrorResponse()


