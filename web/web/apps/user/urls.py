# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.show_user_index_view),
    url(r'^profile/', views.show_user_profile_view),
    url(r'^post-profile', views.post_profile),
)
