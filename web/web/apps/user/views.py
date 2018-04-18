# -*- coding: utf-8 -*-
from django.db.models import Q, F

__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import logging
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from utils import http
from django.contrib.auth.models import User
from course import models as course_models
from user import forms as user_forms
from like import services as like_services
from wish import services as wish_services
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
    form = user_forms.UserProfileForm(instance=request.user.userprofile)
    can_edit_account = request.user.userprofile.user_from == UserFrom.DIRECT_REGISTER.value
    return render_to_response("user/user_edit.html", RequestContext(request, locals()))

@login_required
def user_edit_profile_submit_view(request):
    form = user_forms.UserProfileForm(request.POST, instance=request.user.userprofile)
    if form.is_valid():
        try:
            first_name = form.cleaned_data['first_name']
            user_profile = form.save()
            request.user.first_name = first_name
            request.user.userprofile = user_profile
            request.user.save()
            return http.JsonSuccessResponse()
        except Exception, inst:
            logging.error(str(inst))
    return http.JsonErrorResponse()

@login_required
def user_edit_account_view(request):
    can_edit_account = request.user.userprofile.user_from == UserFrom.DIRECT_REGISTER.value
    return render_to_response("user/user_edit.html", locals())
