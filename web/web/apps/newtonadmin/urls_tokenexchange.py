# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views_tokenexchange

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views_tokenexchange.show_id_list_view),
                       url(r'^id/$', views_tokenexchange.show_id_list_view),
                       url(r'^id/pass/', views_tokenexchange.show_pass_id_list_view),
                       url(r'^id/confirm/', views_tokenexchange.confirm_id),
                       url(r'^invite/(?P<phase_id>[0-9]+)/$', views_tokenexchange.show_invite_view),
                       url(r'^invite/(?P<phase_id>[0-9]+)/post/$', views_tokenexchange.post_invite),
                       url(r'^invite/(?P<phase_id>[0-9]+)/completed/$', views_tokenexchange.show_completed_invite_view),
                       url(r'^invite/(?P<phase_id>[0-9]+)/send/$', views_tokenexchange.send_invite_email),
                       
                       url(r'^amount/(?P<phase_id>[0-9]+)/$', views_tokenexchange.show_amount_list_view),
                       url(r'^amount/(?P<phase_id>[0-9]+)/post/$', views_tokenexchange.post_amount),
                       url(r'^amount/(?P<phase_id>[0-9]+)/completed/$', views_tokenexchange.show_completed_amount_list_view),
                       
                       url(r'^receive/(?P<phase_id>[0-9]+)/$', views_tokenexchange.show_receive_list_view),                    
)
