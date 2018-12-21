# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import json
import random
import time
import datetime
import logging
import calendar
from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.utils import translation
from zinnia.views.entries import EntryDetail
from zinnia.managers import CHINESE, ENGLISH, TYPE_BLOG, TYPE_ANNOUNCEMENT, TYPE_COMMUNITY_VOICE
from zinnia.managers import PUBLISHED

from press.models import PressModel
from subscription import forms as subscription_forms

from utils import http
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification, send_group_notification
from events.views.entries import EntryDetail as EventsEntryDetail
from config import codes

logger = logging.getLogger(__name__)


def show_home_view(request):
    language = translation.get_language()
    language_code = codes.EntryLanguage.ENGLISH.value
    for language_item in settings.LANGUAGE_LIST:
        if language.startswith(language_item[0]):
            language_code = language_item[1]
            break
    presses = PressModel.objects.order_by('-created_at')[0:3]
    entry = EntryDetail()
    activity_entry = entry.get_queryset().filter(language=language_code, status=PUBLISHED,
                                                 entry_type=TYPE_ANNOUNCEMENT, entry_sub_type=0).order_by(
        '-creation_date').first()
    # select operation entry object
    operation_entry = entry.get_queryset().filter(language=language_code, status=PUBLISHED,
                                                  entry_type=TYPE_ANNOUNCEMENT, entry_sub_type__in=[1, 2]).order_by(
        '-creation_date').first()
    # select blog entry object
    blog_entry = entry.get_queryset().filter(language=language_code, status=PUBLISHED,
                                             entry_type=TYPE_BLOG).order_by('-creation_date').first()
    if activity_entry:
        activity_entry.urls = activity_entry.get_absolute_url().replace('/blog/', '/announcement/')
    if operation_entry:
        operation_entry.urls = operation_entry.get_absolute_url().replace('/blog/', '/announcement/')
    if blog_entry:
        blog_entry.urls = blog_entry.get_absolute_url()
    banner_press = PressModel.objects.order_by('-created_at').first()
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    is_index = True
    # events
    event_items = []
    month_range_list = []
    current_month = datetime.date.today()
    events_entries = EventsEntryDetail()
    events_by_language = events_entries.get_queryset().filter(language=language_code).order_by("event_date")
    past_events_list = events_entries.get_queryset().filter(
        language=language_code, event_date__lt=datetime.date.today()).order_by("-event_date")[:6]
    if not events_by_language:
        events_by_language = events_entries.get_queryset().filter(language=codes.EntryLanguage.ENGLISH.value).order_by(
            "event_date")
        past_events_list = events_entries.get_queryset().filter(
            language=codes.EntryLanguage.ENGLISH.value, event_date__lt=datetime.date.today()).order_by("-event_date")[
                           :6]
    coming_events_list = events_by_language.filter(event_date__gte=datetime.date.today())[:6]
    month_list = events_by_language.dates("event_date", "month")
    for each_month in month_list:
        last_day = calendar.monthrange(each_month.year, each_month.month)[-1]
        last_day_month = each_month.replace(day=last_day)
        month_range_list.append((each_month, last_day_month))
    for month_range in month_range_list:
        event_items.append(
            (
                month_range[0],
                events_by_language.filter(event_date__gte=month_range[0], event_date__lte=month_range[1])
            )
        )
    return render(request, 'welcome/index.html', {user: user, 'vapid_key': vapid_key, 'presses': presses,
                                                  'activity_entry': activity_entry, 'operation_entry': operation_entry,
                                                  'blog_entry': blog_entry, 'banner_press': banner_press,
                                                  "current_month": current_month, "event_items": event_items,
                                                  "month_list": month_list,
                                                  "past_events_list": past_events_list,
                                                  "coming_events_list": coming_events_list,
                                                  "is_index": is_index, "language": language})


def show_technology_view(request):
    return render(request, 'welcome/technology.html', locals())


def show_tech_view(request):
    return render(request, 'welcome/tech.html', locals())


def show_team_view(request):
    return render(request, 'welcome/team.html', locals())


def show_about_view(request):
    return render(request, 'welcome/about.html', locals())


def show_joinus_view(request):
    return render(request, 'welcome/joinus.html', locals())


def show_contact_view(request):
    return render(request, 'welcome/contact.html', locals())


def show_register_view(request):
    return render(request, 'welcome/register.html', locals())


def show_mediakit_view(request):
    return render(request, 'welcome/mediakit.html', locals())


def show_protocol_view(request):
    return render(request, 'welcome/protocol.html', locals())


def show_roadmap_view(request):
    return render(request, 'welcome/roadmap.html', locals())


def show_partner_view(request):
    return render(request, 'welcome/partner.html', locals())


def show_announcement_view(request):
    return render(request, 'welcome/announcement.html', locals())


def show_foundation_view(request):
    return render(request, 'welcome/foundation.html', locals())


def show_copyright_view(request):
    return render(request, 'welcome/copyright.html', locals())


def show_terms_of_use_view(request):
    return render(request, 'welcome/terms-of-use.html', locals())


def show_privacy_view(request):
    return render(request, 'welcome/privacy.html', locals())


def show_legal_view(request):
    return render(request, 'welcome/legal.html', locals())


def show_newpay_view(request):
    language = translation.get_language()
    return render(request, 'welcome/newpay.html', locals())


def show_scene_view(request):
    return render(request, 'welcome/scene.html', locals())


def show_business_proposal_view(request):
    return render(request, 'welcome/business-proposal.html', locals())


def show_community_view(request):
    presses = PressModel.objects.order_by('-created_at')[0:4]
    language = translation.get_language()
    language_code = codes.EntryLanguage.ENGLISH.value
    for language_item in settings.LANGUAGE_LIST:
        if language.startswith(language_item[0]):
            language_code = language_item[1]
            break
    entry = EntryDetail()
    # select activity entry object
    activity_entries = entry.get_queryset().filter(language=language_code, status=PUBLISHED,
                                                   entry_type=TYPE_ANNOUNCEMENT, entry_sub_type=0).order_by(
        '-creation_date')[0:4]
    if len(activity_entries) < 4:
        activity_entries = entry.get_queryset().filter(language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED,
                                                       entry_type=TYPE_ANNOUNCEMENT, entry_sub_type=0).order_by(
            '-creation_date')[0:4]
    # select operation entry object
    operation_entries = entry.get_queryset().filter(language=language_code, status=PUBLISHED,
                                                    entry_type=TYPE_ANNOUNCEMENT, entry_sub_type__in=[1, 2]).order_by(
        '-creation_date')[0:4]
    if len(operation_entries) < 4:
        operation_entries = entry.get_queryset().filter(language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED,
                                                        entry_type=TYPE_ANNOUNCEMENT,
                                                        entry_sub_type__in=[1, 2]).order_by('-creation_date')[0:4]
    # select blog entry object
    blog_entries = entry.get_queryset().filter(language=language_code, status=PUBLISHED, entry_type=TYPE_BLOG).order_by(
        '-creation_date')[0:4]
    if len(blog_entries) < 4:
        blog_entries = entry.get_queryset().filter(language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED,
                                                   entry_type=TYPE_BLOG).order_by('-creation_date')[0:4]
    # select community voice entry object
    if language_code == codes.EntryLanguage.CHINESE.value:
        voice_entries = entry.get_queryset().filter(language=codes.EntryLanguage.CHINESE.value, status=PUBLISHED,
                                                    entry_type=TYPE_COMMUNITY_VOICE).order_by('-creation_date')[0:4]
    else:
        voice_entries = entry.get_queryset().filter(language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED,
                                                    entry_type=TYPE_COMMUNITY_VOICE).order_by('-creation_date')[0:4]
    for activity_entry in activity_entries:
        activity_entry.urls = activity_entry.get_absolute_url().replace('/blog/', '/announcement/')
    for operation_entry in operation_entries:
        operation_entry.urls = operation_entry.get_absolute_url().replace('/blog/', '/announcement/')
    for blog_entry in blog_entries:
        blog_entry.urls = blog_entry.get_absolute_url()
    for voice_entry in voice_entries:
        voice_entry.urls = voice_entry.get_absolute_url().replace('/blog/', '/community-voice/')
    return render(request, 'welcome/community.html', locals())


def show_economy_view(request):
    language = translation.get_language()
    arabic_read_style = False
    if language == 'ar':
        arabic_read_style = True
    return render(request, 'welcome/economy.html', locals())


def show_whitepaper_view(request):
    return render(request, 'welcome/whitepaper.html', locals())


def show_wechat_view(request):
    return render(request, 'welcome/wechat.html', locals())


def show_foundation_view(request):
    return render(request, 'welcome/foundation.html', locals())


def show_term_of_service_view(request):
    return render(request, 'welcome/term-of-service.html', locals())


def show_sitemap_view(request):
    return render(request, 'welcome/sitemap.html', locals())


def show_newstatus_view(request):
    return render(request, 'welcome/newstatus.html', locals())


def show_dashboard_view(request):
    return render(request, 'welcome/dashboard.html', locals())


def show_join_partner_view(request):
    return render(request, 'welcome/join-partner.html', locals())


def show_nep_view(request):
    return render(request, 'welcome/nep.html', locals())


def show_newton_community_node_conference_view(request):
    is_chinese = False
    language = translation.get_language()
    if language.startswith("zh"):
        is_chinese = True
    return render(request, 'welcome/newton-community-node-conference.html', locals())


def show_404_page(request):
    return render(request, '404.html')


def show_500_page(request):
    return render(request, '500.html')


class AnnouncementView(generic.ListView):
    template_name = "welcome/announcement.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        language = translation.get_language()
        language_code = codes.EntryLanguage.ENGLISH.value
        for language_item in settings.LANGUAGE_LIST:
            if language.startswith(language_item[0]):
                language_code = language_item[1]
                break
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT, language=language_code, status=PUBLISHED)
        if not entries:
            entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT,
                                                  language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url().replace('/blog/', '/announcement/')
            entry.urls = url
        return entries


class AnnouncementSubView(generic.ListView):
    template_name = "welcome/announcement.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        entry_sub_type = int(self.request.path.split("/")[2])
        language = translation.get_language()
        language_code = codes.EntryLanguage.ENGLISH.value
        for language_item in settings.LANGUAGE_LIST:
            if language.startswith(language_item[0]):
                language_code = language_item[1]
                break
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT, language=language_code,
                                              entry_sub_type=entry_sub_type, status=PUBLISHED)
        if not entries:
            entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT,
                                                  language=codes.EntryLanguage.ENGLISH.value,
                                                  entry_sub_type=entry_sub_type, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url().replace('/blog/', '/announcement/')
            entry.urls = url
        return entries


class AnnouncementDetailView(generic.DetailView):
    template_name = "welcome/announcement-detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT)
        self.get_object(entries)
        return entries


class CommunityVoiceDetailView(generic.DetailView):
    template_name = "welcome/community-voice-detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_COMMUNITY_VOICE)
        self.get_object(entries)
        return entries


class CommunityVoiceView(generic.ListView):
    template_name = "welcome/community-voice.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        language = translation.get_language()
        language_code = codes.EntryLanguage.ENGLISH.value
        for language_item in settings.LANGUAGE_LIST:
            if language.startswith(language_item[0]):
                language_code = language_item[1]
                break
        entry = EntryDetail()
        if language_code == codes.EntryLanguage.CHINESE.value:
            entries = entry.get_queryset().filter(entry_type=TYPE_COMMUNITY_VOICE,
                                                  language=codes.EntryLanguage.CHINESE.value, status=PUBLISHED)
        else:
            entries = entry.get_queryset().filter(entry_type=TYPE_COMMUNITY_VOICE,
                                                  language=codes.EntryLanguage.ENGLISH.value, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url().replace('/blog/', '/community-voice/')
            entry.urls = url
        return entries
