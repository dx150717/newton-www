# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                    url(r'^session/$', views.check_session_auth),
)
