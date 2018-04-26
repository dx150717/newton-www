# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_kyc.kyc_admin),
                    url(r'^id-confirm/$', views_kyc.kyc_id_confirm),
                    url(r'^amount-confirm/$', views_kyc.kyc_amount_confirm),
                    url(r'^email-confirm/$', views_kyc.kyc_email_confirm),
                    url(r'^email-list/$', views_kyc.kyc_email_list),
                    url(r'^step-one/', views_kyc.kyc_step_one),
                    url(r'^step-two/', views_kyc.kyc_step_two),
                    url(r'^step-three/', views_kyc.kyc_step_three),
                    url(r'^update-id/', views_kyc.kyc_update_id),
                    url(r'^update-amount/', views_kyc.kyc_update_amount),
                    url(r'^update-email/', views_kyc.kyc_update_email),
                    url(r'^send-one-email/', views_kyc.kyc_send_one_email),
                    url(r'^send-email/', views_kyc.kyc_send_email),
                    url(r'^export-csv/', views_kyc.kyc_export_csv),
)
