from django.conf.urls import patterns, include, url
# -*- coding: utf-8 -*-
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
                    url(r'^$', views.show_index_view),
                    url(r'^login/$', views.show_login_view),
                    url(r'^login/post/$', views.post_login),
                    url(r'^logout/$', views.show_logout_view),
                    url(r'^kyc/', include('newtonadmin.urls_kyc')),
)
