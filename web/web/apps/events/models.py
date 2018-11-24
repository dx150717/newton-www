# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'

from django.db import models
from django.utils import timezone

from config import codes


class EventModel(models.Model):
    """
    Entry of press.
    """
    LANGUAGE_CHOICES = (
        (codes.EntryLanguage.CHINESE.value, u"汉语"),
        (codes.EntryLanguage.ENGLISH.value, u"英语"),
    )

    event_title = models.CharField(max_length=200, verbose_name=u'活动标题')
    event_during = models.CharField(max_length=200, verbose_name=u'活动持续时间')
    event_date = models.DateField(default=timezone.now, verbose_name=u'活动开始日期')
    event_summary = models.TextField(verbose_name=u'活动简介')
    event_img = models.FileField(upload_to='uploads/event/%Y/%m/%d', verbose_name=u'活动图片')
    event_link = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'活动链接')
    event_language = models.IntegerField(choices=LANGUAGE_CHOICES, verbose_name=u'选择语言')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    def __str__(self):
        return self.event_title

    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = verbose_name
