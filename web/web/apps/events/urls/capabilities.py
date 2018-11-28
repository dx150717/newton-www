"""Urls for the zinnia capabilities"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.views.capabilities import RsdXml
from events.views.capabilities import HumansTxt
from events.views.capabilities import OpenSearchXml
from events.views.capabilities import WLWManifestXml


urlpatterns = patterns(
    '',
    url(r'^rsd.xml$', RsdXml.as_view(),
        name='rsd'),
    url(r'^humans.txt$', HumansTxt.as_view(),
        name='humans'),
    url(r'^opensearch.xml$', OpenSearchXml.as_view(),
        name='opensearch'),
    url(r'^wlwmanifest.xml$', WLWManifestXml.as_view(),
        name='wlwmanifest')
)
