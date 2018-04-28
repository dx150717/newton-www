# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

from utils import http
from config import codes
from kyc import models as kyc_models
from . import forms_kyc
from . import services_kyc

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_id_list_view(request):
    """Show the candiate ID list
    
    """
    try:
        items = kyc_models.KYCInfo.objects.filter(status=codes.KYCStatus.CANDIDATE.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/id-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show id list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_id(request):
    """Confirm whether ID is valid
    
    """
    try:
        form = forms_kyc.ConfirmKYCForm(request.POST)
        if not form.is_valid():
            return http.HttpResponseServerError()
        user_id = int(form.cleaned_data['user_id'])
        pass_kyc = int(form.cleaned_data['pass_kyc'])
        level = int(form.cleaned_data['level'])
        item = kyc_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CANDIDATE.value, phase_id=settings.CURRENT_FUND_PHASE)
        if pass_kyc:
            item.status = codes.KYCStatus.CONFIRM.value
            item.level = level
        else:
            item.status = codes.KYCStatus.CANCEL.value
        item.save()
        return redirect('/newtonadmin/kyc/id/')
    except Exception, inst:
        logger.exception("fail to confirm id:%s" % str(inst))
        return http.HttpResponseNotFound()        

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_amount_list_view(request):
    """Show the investor list which we don't set the invest amount
    
    """
    try:
        items = kyc_models.KYCInfo.objects.filter(status=codes.KYCStatus.CONFIRM.value, phase_id=settings.CURRENT_FUND_PHASE)
        return render(request, "newtonadmin/amount-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show amount list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_amount(request):
    """Show the investor list which we don't set the invest amount
    
    """
    try:
        form = forms.AmountForm(request.POST)
        if not form.is_valid():
            return http.HttpResponseServerError()
        user_id = int(form.cleaned_data['user_id'])
        min_btc_limit = int(form.cleaned_data['min_btc_limit'])
        max_btc_limit = int(form.cleaned_data['min_btc_limit'])
        min_ela_limit = int(form.cleaned_data['min_ela_limit'])
        max_ela_limit = int(form.cleaned_data['min_ela_limit'])
        # Query the available address
        btc_address = services_kyc.allocate_btc_address()
        ela_address = services_kyc.allocate_ela_address()
        if not btc_address or not ela_address:
            return http.HttpResponseServerError()
        distribute_item = kyc_models.DistributionInfo.objects.filter(user__id=user_id, phase_id=settings.CURRENT_FUND_PHASE).first()
        if not distribute_item:
            distribute_item = kyc_models.DistributionInfo()
            distribute_item.user_id = user_id
            distribute_item.phase_id = settings.CURRENT_FUND_PHASE
        distribute_item.min_btc_limit = min_btc_limit
        distribute_item.max_btc_limit = max_btc_limit
        distribute_item.min_ela_limit = min_ela_limit
        distribute_item.max_ela_limit = max_ela_limit
        distribute_item.receive_btc_address = btc_address
        distribute_item.receive_ela_address = ela_address
        distribute_item.save()
        # save status
        item = kyc_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CONFIRM.value, phase_id=settings.CURRENT_FUND_PHASE)
        item.status = codes.KYCStatus.DISTRIBUTE.value
        item.save()
        return redirect('/newtonadmin/kyc/amount/')
    except Exception, inst:
        logger.exception("fail to confirm amount:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_email_list_view(request):
    """Show the investor list which we don't send the final email to
    
    """
    return render(request, "newtonadmin/email-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_email(request, user_id):
    """Determine whether send email to investor
    
    """
    try:
        pass
    except Exception, inst:
        logger.exception("fail to confirm email:%s" % str(inst))
        return http.HttpResponseServerError()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_sent_list_view(request):
    """Show the investor list which we have already sent the final email to
    
    """
    return render(request, "newtonadmin/email-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def export_file(request):
    """Export the final investor list to file
    
    """
    pass
