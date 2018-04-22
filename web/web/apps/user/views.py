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


logger = logging.getLogger(__name__)


def user_view(request, user_id=None):
    if user_id:
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
    else:
        user = request.user
        if not user.is_authenticated():
            return redirect('/login/')
    all_courses = []
    resource_ids = like_services.get_like_resource_ids(user, codes.ResourceType.COURSE.value)
    like_courses = course_models.Course.objects.filter(id__in=resource_ids, status=codes.StatusCode.AVAILABLE.value)
    if like_courses:
        all_courses.extend(like_courses)
    resource_ids = wish_services.get_wish_resource_ids(user, codes.ResourceType.COURSE.value)
    wish_courses = course_models.Course.objects.filter(id__in=resource_ids, status=codes.StatusCode.AVAILABLE.value)
    if wish_courses:
        all_courses.extend(wish_courses)
    all_courses = list(set(all_courses))
    return render_to_response("user/index.html", locals())


@login_required
def user_edit_profile_view(request):
    return render(request, "user/user_edit.html", locals())

@login_required
def user_edit_profile_submit_view(request):
    if request.method == "POST":
        try:
            # homepage = request.POST['homepage']
            # country_code = request.POST['country_code']
            # gender = request.POST['gender']
            # print("gender? %s" %gender)
            # cellphone = request.POST['cellphone']
            # job_status = request.POST['job_status']
            # construction_mode = request.POST['construction_mode']
            # newton_channel = request.POST['newton_channel']
            # #validate data
            # profile = user_model.UserProfile(user=request.user,homepage=homepage,
            # country_code=country_code,gender=int(gender.encode("utf-8")),cellphone=cellphone,
            # job_status=int(job_status.encode("utf-8")),construction_mode=int(construction_mode.encode("utf-8")),channel="test"
            # )
            # profile.save()
            return redirect("/")
        except Exception, inst:
            print("error: %s" %str(inst))
    return http.JsonErrorResponse()

@login_required
def user_edit_account_view(request):
    can_edit_account = request.user.userprofile.user_from == UserFrom.DIRECT_REGISTER.value
    return render_to_response("user/user_edit.html", locals())
