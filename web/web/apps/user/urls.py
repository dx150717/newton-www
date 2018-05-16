# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.show_user_index_view),
    url(r'^token-exchange-progress/(?P<phase_id>[0-9]+)/', views.show_token_exchange_progress_view),
)
