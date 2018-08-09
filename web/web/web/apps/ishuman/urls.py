# -*- coding: utf-8 -*-
from django.conf.urls import *

urlpatterns = patterns('ishuman.views',
                       (r'^image/$', 'show_captcha_image'),
                       (r'^check/$', 'check_captcha'),
)
