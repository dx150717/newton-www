# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_kyc

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_kyc.show_id_list_view),
                    url(r'^id/$', views_kyc.show_id_list_view),
                    url(r'^id/confirm/', views_kyc.confirm_id),

                    url(r'^amount/$', views_kyc.show_amount_list_view),
                    url(r'^amount/confirm/', views_kyc.confirm_amount),

                    url(r'^email/$', views_kyc.show_email_list_view),
                    url(r'^email/confirm/', views_kyc.confirm_email),

                    url(r'^sent/$', views_kyc.show_sent_list_view),                    
                    
                    url(r'^export/', views_kyc.export_file),
)
