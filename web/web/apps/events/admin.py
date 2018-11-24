# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'

from django.contrib import admin
from . import models
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class EventsAdmin(admin.ModelAdmin):
    fields = ('event_title', 'event_date', 'event_during', 'event_summary', 'event_img', 'event_link', 'event_language')
    list_display = ('event_title', 'event_date', 'event_during', 'event_summary', 'event_img', 'event_link', 'event_language')


admin.site.register(models.EventModel, EventsAdmin)
