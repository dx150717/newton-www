# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.show_tokensale_index_view),
	url(r'^join/$', views.show_join_tokensale_view),
	url(r'^post/$', views.post_kyc_information),
	url(r'^wait-audit/$', views.show_wait_audit_view),
	url(r'^verify/$', views.verify_email_link),
	url(r'^limit-address/$', views.show_limit_and_address_view),
	url(r'^invalid-link/$', views.show_invalid_link),
)
