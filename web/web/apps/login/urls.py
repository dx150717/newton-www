# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_login_view),
                    url(r'^post/', views.post_login, name="post_login"),
)
