# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'


from tinymce.widgets import TinyMCE

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import Media

from . import models


class EventsAdmin(admin.ModelAdmin):
    fields = ('event_title', 'event_date', 'event_during', 'event_summary', 'content', 'event_img', 'event_link',
              'event_language')
    list_display = ('event_title', 'event_date', 'event_during', 'event_link', 'event_language')


admin.site.register(models.EventModel, EventsAdmin)


class EventsAdminTinyMCEMixin(object):
    """
    Mixin adding TinyMCE for editing Entry.content field.
    """

    def _media(self):
        """
        The medias needed to enhance the admin page.
        """
        media = super(EventsAdminTinyMCEMixin, self).media

        media += TinyMCE().media + Media(
            js=[reverse('tinymce-js', args=['admin/zinnia/entry']),
                reverse('tinymce-filebrowser-callback')]
        )

        return media

    media = property(_media)


class EventsAdminTinyMCE(EventsAdminTinyMCEMixin, EventsAdmin):
    """
    Enrich the default EntryAdmin with TinyMCE.
    """
    pass


admin.site.unregister(models.EventModel)
admin.site.register(models.EventModel, EventsAdminTinyMCE)
