"""Urls for the Zinnia feeds"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.urls import _
from events.feeds import LatestEntries
from events.feeds import TagEntries
from events.feeds import AuthorEntries
from events.feeds import CategoryEntries
from events.feeds import SearchEntries
from events.feeds import EntryComments
from events.feeds import EntryPingbacks
from events.feeds import EntryTrackbacks
from events.feeds import EntryDiscussions
from events.feeds import LatestDiscussions


urlpatterns = patterns(
    '',
    url(r'^$',
        LatestEntries(),
        name='entry_latest_feed'),
    url(_(r'^discussions/$'),
        LatestDiscussions(),
        name='discussion_latest_feed'),
    url(_(r'^search/$'),
        SearchEntries(),
        name='entry_search_feed'),
    url(_(r'^tags/(?P<tag>[^/]+(?u))/$'),
        TagEntries(),
        name='tag_feed'),
    url(_(r'^authors/(?P<username>[.+-@\w]+)/$'),
        AuthorEntries(),
        name='author_feed'),
    url(_(r'^categories/(?P<path>[-\/\w]+)/$'),
        CategoryEntries(),
        name='category_feed'),
    url(_(r'^discussions/(?P<year>\d{4})/(?P<month>\d{2})/'
          '(?P<day>\d{2})/(?P<slug>[-\w]+)/$'),
        EntryDiscussions(),
        name='entry_discussion_feed'),
    url(_(r'^comments/(?P<year>\d{4})/(?P<month>\d{2})/'
          '(?P<day>\d{2})/(?P<slug>[-\w]+)/$'),
        EntryComments(),
        name='entry_comment_feed'),
    url(_(r'^pingbacks/(?P<year>\d{4})/(?P<month>\d{2})/'
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$'),
        EntryPingbacks(),
        name='entry_pingback_feed'),
    url(_(r'^trackbacks/(?P<year>\d{4})/(?P<month>\d{2})/'
        '(?P<day>\d{2})/(?P<slug>[-\w]+)/$'),
        EntryTrackbacks(),
        name='entry_trackback_feed'),
)
