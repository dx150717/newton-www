# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_admin(request):
    return render(request, "newtonadmin/kycindex.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_id_confirm(request):
    return render(request, "newtonadmin/kyc-id-confirm.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_amount_confirm(request):
    return render(request, "newtonadmin/kyc-amount-confirm.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_email_confirm(request):
    return render(request, "newtonadmin/kyc-email-confirm.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_email_list(request):
    return render(request, "newtonadmin/kyc-email-list.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_step_one(request):
    return render(request, "newtonadmin/kyc-step-one.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_step_two(request):
    return render(request, "newtonadmin/kyc-step-two.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_step_three(request):
    return render(request, "newtonadmin/kyc-step-three.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_update_id(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/kyc-step-one.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_update_amount(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/kyc-step-two.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_update_email(request):
    update_info = "Send Successed!"
    return render(request, "newtonadmin/kyc-step-three.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_send_one_email(request):
    update_info = "Send Successed!"    
    return render(request, "newtonadmin/kyc-step-three.html", locals())

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_send_email(request):
    update_info = "Send Successed!"    
    return render(request, "newtonadmin/kycindex.html", locals());

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def kyc_export_csv(request):
    update_info = "Export Successed!"
    return render(request, "newtonadmin/kycindex.html", locals());

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def blog_admin(request):
    return render(request, "index.html", locals())
