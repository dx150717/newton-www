# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_tokenexchange

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views_tokenexchange.show_id_list_view),
                    url(r'^id/$', views_tokenexchange.show_id_list_view),
                    url(r'^id/confirm/', views_tokenexchange.confirm_id),

                    url(r'^amount/$', views_tokenexchange.show_amount_list_view),
                    url(r'^amount/confirm/', views_tokenexchange.confirm_amount),

                    url(r'^email/$', views_tokenexchange.show_email_list_view),
                    url(r'^email/confirm/', views_tokenexchange.confirm_email),

                    url(r'^sent/$', views_tokenexchange.show_sent_list_view),                    

                    url(r'^receive/$', views_tokenexchange.show_receive_list_view),                    
)
