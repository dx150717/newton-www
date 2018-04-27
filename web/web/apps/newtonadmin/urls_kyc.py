# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_kyc

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_kyc.show_filter_id_list_view),
                    url(r'^filter-id-list/$', views_kyc.show_filter_id_list_view),
                    url(r'^confirm-id/(?P<user_id>[0-9]+)/', views_kyc.confirm_id),

                    url(r'^filter-amount-list/$', views_kyc.show_filter_amount_list_view),
                    url(r'^filter-amount-detail/', views_kyc.show_filter_amount_detail_view),
                    url(r'^confirm-amount/', views_kyc.confirm_amount),

                    url(r'^filter-email-confirm/$', views_kyc.show_filter_email_list_view),
                    url(r'^filter-email-detail/', views_kyc.show_filter_email_detail_view),
                    url(r'^confirm-email/', views_kyc.confirm_email),

                    url(r'^email-list/$', views_kyc.show_email_list_view),                    
                    url(r'^send-batch-email/', views_kyc.send_batch_email),
                    
                    url(r'^export-csv/', views_kyc.export_csv),
)
