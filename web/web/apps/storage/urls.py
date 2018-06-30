# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                    url(r'^protect/(?P<path>.*)$', views.check_file_permission),
)
