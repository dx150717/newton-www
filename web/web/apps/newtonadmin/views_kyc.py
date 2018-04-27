# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_admin(request):
    return render(request, "newtonadmin/kycindex.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_id_list_view(request):
    return render(request, "newtonadmin/filter-id-list.html", locals())

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
def show_filter_id_detail_view(request):
    return render(request, "newtonadmin/filter-id-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_amount_detail_view(request):
    return render(request, "newtonadmin/filter-amount-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_filter_email_detail_view(request):
    return render(request, "newtonadmin/filter-email-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def comfirm_id(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/filter-id-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def comfirm_amount(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/filter-amount-detail.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def comfirm_email(request):
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
