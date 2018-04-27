# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_kyc

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_kyc.kyc_admin),
                    url(r'^filter-id-list/$', views_kyc.show_filter_id_list_view),
                    url(r'^filter-amount-list/$', views_kyc.show_filter_amount_list_view),
                    url(r'^filter-email-confirm/$', views_kyc.show_filter_email_list_view),
                    url(r'^email-list/$', views_kyc.show_email_list_view),
                    url(r'^filter-id-detail/', views_kyc.show_filter_id_detail_view),
                    url(r'^filter-amount-detail/', views_kyc.show_filter_amount_detail_view),
                    url(r'^filter-email-detail/', views_kyc.show_filter_email_detail_view),
                    url(r'^comfirm-id/', views_kyc.comfirm_id),
                    url(r'^comfirm-amount/', views_kyc.comfirm_amount),
                    url(r'^comfirm-email/', views_kyc.comfirm_email),
                    url(r'^send-batch-email/', views_kyc.send_batch_email),
                    url(r'^export-csv/', views_kyc.export_csv),
)
