# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'

import logging

from django import template

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(name='format_current_month')
def format_current_month(date_time):
    """format upgrade message"""
    try:
        return date_time.strftime("%B %Y")
    except Exception, inst:
        logger.exception("fail to format current month: %s" % str(inst))
        return ""


@register.filter(name='format_event_month')
def format_event_month(date_time):
    """format upgrade message"""
    try:
        return date_time.strftime("%b")
    except Exception, inst:
        logger.exception("fail to format event month: %s" % str(inst))
        return ""


@register.filter(name='format_event_weekday')
def format_event_weekday(date_time):
    """format upgrade message"""
    try:
        return date_time.strftime("%a").upper()
    except Exception, inst:
        logger.exception("fail to format event weekday: %s" % str(inst))
        return ""


@register.filter(name='get_event_url')
def get_event_url(event):
    """format upgrade message"""
    try:
        if event.event_link:
            return 'target=_blank href=%s' % event.event_link
        elif event.content:
            return 'target=_blank href=%s' % event.get_absolute_url()
    except Exception, inst:
        logger.exception("fail to get event url: %s" % str(inst))
        return ""
