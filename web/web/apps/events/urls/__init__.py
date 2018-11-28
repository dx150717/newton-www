"""Defaults urls for the Zinnia project"""
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

from django.utils.translation import ugettext_lazy

from events.settings import TRANSLATED_URLS


def i18n_url(url, translate=TRANSLATED_URLS):
    """
    Translate or not an URL part.
    """
    if translate:
        return ugettext_lazy(url)
    return url

_ = i18n_url

urlpatterns = patterns(
    '',
    url(_(r'^feeds/'), include('events.urls.feeds')),
    url(_(r'^tags/'), include('events.urls.tags')),
    url(_(r'^authors/'), include('events.urls.authors')),
    url(_(r'^categories/'), include('events.urls.categories')),
    url(_(r'^search/'), include('events.urls.search')),
    url(_(r'^random/'), include('events.urls.random')),
    url(_(r'^sitemap/'), include('events.urls.sitemap')),
    url(_(r'^trackback/'), include('events.urls.trackback')),
    url(_(r'^comments/'), include('events.urls.comments')),
    url(r'^', include('events.urls.entries')),
    url(r'^', include('events.urls.archives')),
    url(r'^', include('events.urls.shortlink')),
    url(r'^', include('events.urls.quick_entry')),
    url(r'^', include('events.urls.capabilities')),
)
