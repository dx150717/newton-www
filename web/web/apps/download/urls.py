# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^newpay/mainnet/$', views.show_newpay_download_view),
                       url(r'^newpay/guide/$', views.show_newpay_guide_view),
                       )