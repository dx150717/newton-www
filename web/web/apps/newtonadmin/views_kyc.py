# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from utils import http
from config import codes
from kyc import models as kyc_models
from . import forms_kyc

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_id_list_view(request):
    try:
        id_list = kyc_models.KYCInfo.objects.filter(status=codes.KYCStatus.CANDIDATE.value)
        return render(request, "newtonadmin/filter-id-list.html", locals())
    except Exception, inst:
        logger.exception("fail to show filter id list:%s" % str(inst))
        return http.HttpResponseServerError()    

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_id_detail_view(request, user_id):
    try:
        user_id = int(user_id)
        item = kyc_models.KYCInfo.objects.get(user__id=user_id, status=codes.KYCStatus.CANDIDATE.value)
        return render(request, "newtonadmin/filter-id-detail.html", locals())
    except Exception, inst:
        logger.exception("fail to show filter id detail:%s" % str(inst))
        return http.HttpResponseNotFound()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_id(request, user_id):
    try:
        user_id = int(user_id)
        form = forms_kyc.IDConfirmForm(request.POST)
        if not form.is_valid():
            return http.HttpResponseServerError()
        pass_kyc = form.cleaned_data['pass_kyc']
        print "pass_kyc", pass_kyc
        update_info = "Update Successed!"
        return render(request, "newtonadmin/filter-id-detail.html", locals())
    except Exception, inst:
        logger.exception("fail to show filter id detail:%s" % str(inst))
        return http.HttpResponseServerError()        

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_amount_list_view(request):
    return render(request, "newtonadmin/filter-amount-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_email_list_view(request):
    return render(request, "newtonadmin/filter-email-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_email_list_view(request):
    return render(request, "newtonadmin/email-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_amount_detail_view(request):
    return render(request, "newtonadmin/filter-amount-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_email_detail_view(request):
    return render(request, "newtonadmin/filter-email-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_amount(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/filter-amount-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_email(request):
    update_info = "Send Successed!"
    return render(request, "newtonadmin/filter-email-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def send_batch_email(request):
    update_info = "Send Successed!"    
    return render(request, "newtonadmin/kycindex.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def export_csv(request):
    update_info = "Export Successed!"
    return render(request, "newtonadmin/kycindex.html", locals());

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def blog_admin(request):
    return render(request, "index.html", locals())
