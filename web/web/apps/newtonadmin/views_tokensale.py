# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from utils import http
from config import codes
from tokensale import models as tokensale_models
from . import forms_tokensale
from . import services_tokensale

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_id_list_view(request):
    """Show the candiate ID list
    
    """
    try:
        items = tokensale_models.KYCInfo.objects.filter(status=codes.KYCStatus.CANDIDATE.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/id-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show id list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_id(request):
    """Confirm whether ID is valid
    
    """
    try:
        form = forms_tokensale.ConfirmKYCForm(request.POST)
        if not form.is_valid():
            return http.HttpResponseServerError()
        user_id = int(form.cleaned_data['user_id'])
        pass_tokensale = int(form.cleaned_data['pass_kyc'])
        level = int(form.cleaned_data['level'])
        item = tokensale_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CANDIDATE.value, phase_id=settings.CURRENT_FUND_PHASE)
        if pass_tokensale:
            item.status = codes.KYCStatus.CONFIRM.value
            item.level = level
        else:
            item.status = codes.KYCStatus.CANCEL.value
        item.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to confirm id:%s" % str(inst))
        return http.JsonErrorResponse()        

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_amount_list_view(request):
    """Show the investor list which we don't set the invest amount
    
    """
    try:
        items = tokensale_models.KYCInfo.objects.filter(status=codes.KYCStatus.CONFIRM.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/amount-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show amount list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_amount(request):
    """Show the investor list which we don't set the invest amount
    
    """
    try:
        form = forms_tokensale.AmountForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        min_btc_limit = int(form.cleaned_data['min_btc_limit'])
        max_btc_limit = int(form.cleaned_data['min_btc_limit'])
        min_ela_limit = int(form.cleaned_data['min_ela_limit'])
        max_ela_limit = int(form.cleaned_data['min_ela_limit'])
        # Query the available address
        btc_address = services_tokensale.allocate_btc_address()
        ela_address = services_tokensale.allocate_ela_address()
        if not btc_address or not ela_address:
            return http.JsonErrorResponse()
        # save status
        item = tokensale_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CONFIRM.value, phase_id=settings.CURRENT_FUND_PHASE)
        item.status = codes.KYCStatus.DISTRIBUTE.value
        item.min_btc_limit = min_btc_limit
        item.max_btc_limit = max_btc_limit
        item.min_ela_limit = min_ela_limit
        item.max_ela_limit = max_ela_limit
        item.receive_btc_address = btc_address
        item.receive_ela_address = ela_address
        item.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to confirm amount:%s" % str(inst))
        return http.JsonErrorResponse()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_email_list_view(request):
    """Show the investor list which we don't send the final email to
    
    """
    try:
        items = tokensale_models.KYCInfo.objects.filter(status=codes.KYCStatus.DISTRIBUTE.value, phase_id=settings.CURRENT_FUND_PHASE)
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
        item = tokensale_models.KYCInfo.objects.filter(user__id=user_id, status=codes.KYCStatus.DISTRIBUTE.value, phase_id=settings.CURRENT_FUND_PHASE).first()
        if not item:
            logger.error("item is not found.")
            return http.JsonErrorResponse()
        if services_tokensale.send_distribution_letter(item.user):
            item.status = codes.KYCStatus.SENT.value
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
        items = tokensale_models.KYCInfo.objects.filter(status=codes.KYCStatus.SENT.value, phase_id=settings.CURRENT_FUND_PHASE).order_by('-created_at')
        return render(request, "newtonadmin/sent-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show sent list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_receive_list_view(request):
    """Show the investor list who send money to newton foundation
    
    """
    try:
        items = tokensale_models.AddressTransaction.objects.filter(phase_id=settings.CURRENT_FUND_PHASE).order_by('-created_at')
        return render(request, "newtonadmin/receive-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show sent list:%s" % str(inst))
        return http.HttpResponseServerError()    

