"""Urls for the Zinnia authors"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.urls import _
from events.views.authors import AuthorList
from events.views.authors import AuthorDetail


urlpatterns = patterns(
    '',
    url(r'^$',
        AuthorList.as_view(),
        name='author_list'),
    url(_(r'^(?P<username>[.+-@\w]+)/page/(?P<page>\d+)/$'),
        AuthorDetail.as_view(),
        name='author_detail_paginated'),
    url(r'^(?P<username>[.+-@\w]+)/$',
        AuthorDetail.as_view(),
        name='author_detail'),
)
