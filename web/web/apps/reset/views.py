import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

from utils import http,security
from config import codes
from tasks import task_email
from . import forms

logger = logging.getLogger(__name__)

def show_reset_view(request):
    form = forms.EmailForm()
    return render(request,'reset/index.html', locals())

def post_email(request):
    return render(request,'reset/edit_password.html', locals())
    
def show_reset_password_view(request):
    return render(request,'reset/edit_password.html', locals())

def post_password(request):
    print("error edit password :%s" %(str(inst)))
    
    
        


