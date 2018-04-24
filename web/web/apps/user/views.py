# -*- coding: utf-8 -*-
from django.db.models import Q, F

__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from utils import http
from django.contrib.auth.models import User
from user import models as user_model
from config import codes
from forms import UserProfileForm

logger = logging.getLogger(__name__)


@login_required
def user_view(request, user_id=None):
    id = request.user.id
    print("user id :%s" %(str(id)) )
    profile_instance = user_model.UserProfile.objects.filter(user_id=int(id)).first()
    form = UserProfileForm(instance=profile_instance)
    return render(request, "user/index.html", locals()) 


@login_required
def user_edit_profile_view(request):
    form = UserProfileForm()
    id = request.user.id
    return render(request, "user/user_edit2.html", locals())

@login_required
def user_edit_profile_submit_view(request):
    return redirect("/")
    if request.method == "POST":
        try:
            user_id = request.POST['id']
            user_id = int(user_id)
            profile_instance = user_model.UserProfile.objects.get(user_id=user_id)
            if profile_instance is None:
                return redirect("/register/")
            else:
                form = UserProfileForm(request.POST, instance=profile_instance)
                if form.is_valid():
                    form.save()
                    return render("/")
                else:
                    return render(request, "user/user_edit2.html", locals())
        except Exception, inst:
            print("error:%s" %str(inst))
            return redirect("/")

@login_required
def user_edit_account_view(request):
    can_edit_account = request.user.userprofile.user_from == UserFrom.DIRECT_REGISTER.value
    return render_to_response("user/user_edit.html", locals())

@login_required
def kyc_view(request):
    return render(request, "user/kyc.html", locals())
