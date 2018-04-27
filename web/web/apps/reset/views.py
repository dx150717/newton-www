import logging
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.timezone import utc
from django.conf import settings

from utils import http
from utils import security
from config import codes
from tasks import task_email

import decorators
from . import forms
from . import services

logger = logging.getLogger(__name__)

def show_reset_view(request):
    form = forms.EmailForm()
    return render(request,'reset/index.html', locals())

@decorators.http_post_required
def post_email(request):
    try:
        form = forms.EmailForm(request.POST)
        if not form.is_valid():
            return render(request,'reset/index.html', locals())
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            # no user TODO tips: 
            return http.HttpResponseRedirect('/reset/post-fail/')
        is_send_success = services.send_reset_validate_email(email, request)
        if not is_send_success:
            return http.HttpResponseRedirect('/reset/post-fail/')
        else:
            return http.HttpResponseRedirect('/reset/post-success/')
    except Exception, inst:
        logger.exception("fail to post email %s" % str(inst))
    return http.HttpResponseServerError()
    
def show_post_success_view(request):
    return render(request,'reset/reset-success.html', locals())

def show_post_fail_view(request):
    return render(request,'reset/reset-fail.html', locals())

def verify_email_link(request):
    try:
        uuid = request.GET['uuid']
        verification = services.get_reset_verification_by_uuid(uuid)
        if not verification:
            return http.HttpResponseRedirect('/reset/invalid-link/')
        email = verification.email_address
        expire_time = verification.expire_time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if now > expire_time:
            return http.HttpResponseRedirect('/reset/invalid-link/')
        # check user
        user = User.objects.filter(email=email).first()
        if not user:
            return http.HttpResponseRedirect('/reset/invalid-link/')
        return http.HttpResponseRedirect('/reset/reset-password/')
    except Exception, inst:
        logger.exception("fail to verify reset link: %s" % str(inst))
        return http.HttpResponseRedirect('/reset/invalid-link/')

def show_invalid_link_view(request):
    return render(request,'reset/invalid-link.html', locals())

def show_reset_password_view(request):
    form = forms.PasswordForm()
    return render(request,'reset/edit_password.html', locals())

@decorators.http_post_required
def post_password(request):
    try:
        form = forms.PasswordForm(request.POST)
        if not form.is_valid():
            return render(request,'reset/edit_password.html', locals()) 
        password = form.cleaned_data['password']
        repassword = form.cleaned_data['repassword']
        if password != repassword:
            return http.HttpResponseRedirect('/reset/post-fail/')
        id = request.user.id
        user = User.objects.filter(id=id).first()
        if not user:
            return http.HttpResponseRedirect('/reset/post-fail/')
        user.set_password(password)
        user.save()
        return http.HttpResponseRedirect('/login/')
    except Exception, inst:
        logger.exception("fail to reset password: %s" %str(inst))
        return render(request,'reset/edit_password.html', locals())
    
    
        


