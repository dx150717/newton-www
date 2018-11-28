"""Urls for the Zinnia tags"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.urls import _
from events.views.tags import TagList
from events.views.tags import TagDetail


urlpatterns = patterns(
    '',
    url(r'^$',
        TagList.as_view(),
        name='tag_list'),
    url(r'^(?P<tag>[^/]+(?u))/$',
        TagDetail.as_view(),
        name='tag_detail'),
    url(_(r'^(?P<tag>[^/]+(?u))/page/(?P<page>\d+)/$'),
        TagDetail.as_view(),
        name='tag_detail_paginated'),
)
