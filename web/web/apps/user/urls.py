# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from . import views
from config import codes

urlpatterns = patterns('',
    url(r'^$', views.show_user_index_view, {"active_page": codes.UserCenterActivePage.KYCACTIVE.value}),
    url(r'^tokenexchange/$', views.show_user_index_view, {"active_page": codes.UserCenterActivePage.TOKENEXCHANGEACTIVE.value}),
)
