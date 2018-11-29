"""Urls for the Zinnia comments"""
from django.conf.urls import url
from django.conf.urls import patterns

from events.urls import _
from events.views.comments import CommentSuccess


urlpatterns = patterns(
    '',
    url(_(r'^success/$'),
        CommentSuccess.as_view(),
        name='comment_success')
)
