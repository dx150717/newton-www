# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.show_kyc_information_view),
	url(r'^post/$', views.post_kyc_information),
	url(r'^wait-audit/$', views.show_wait_audit_view),
)
