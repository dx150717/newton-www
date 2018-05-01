# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_tokensale

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_tokensale.show_id_list_view),
                    url(r'^id/$', views_tokensale.show_id_list_view),
                    url(r'^id/confirm/', views_tokensale.confirm_id),

                    url(r'^amount/$', views_tokensale.show_amount_list_view),
                    url(r'^amount/confirm/', views_tokensale.confirm_amount),

                    url(r'^email/$', views_tokensale.show_email_list_view),
                    url(r'^email/confirm/', views_tokensale.confirm_email),

                    url(r'^sent/$', views_tokensale.show_sent_list_view),                    

                    url(r'^receive/$', views_tokensale.show_receive_list_view),                    
)
