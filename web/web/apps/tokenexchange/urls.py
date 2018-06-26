# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from . import views
from config import codes

urlpatterns = patterns('',
                       url(r'^$', views.show_tokenexchange_index_view),
                       url(r'^individual/post/$', views.post_kyc_information, {"kyc_type": codes.KYCType.INDIVIDUAL.value}),
                       url(r'^organization/post/$', views.post_kyc_information, {"kyc_type": codes.KYCType.ORGANIZATION.value}),
                       url(r'^wait-audit/$', views.show_wait_audit_view),
                       url(r'^invalid-link/$', views.show_invalid_link),
                       url(r'^pending/', views.show_pending_view),
                       url(r'^end/', views.show_end_view),
                       url(r'^invite/(?P<invite_id>[0-9]+)/post/$', views.post_apply_amount),
                       url(r'^invite/(?P<invite_id>[0-9]+)/success/$', views.show_apply_success),
                       url(r'^(?P<invite_id>[0-9]+)/$', views.show_receive_address_view),
)
