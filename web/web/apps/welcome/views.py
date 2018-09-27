# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import json
import random
import time
import datetime
import logging
from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.utils import translation
from zinnia.views.entries import EntryDetail
from zinnia.managers import CHINESE,ENGLISH,TYPE_BLOG,TYPE_ANNOUNCEMENT,KOREAN,JAPANESE,RUSSIAN,TURKISH,SPANISH,FRENCH,GERMAN,ARABIC,NETHERLAND,FINNISH,INDONESIAN,ITALY,THAILAND
from zinnia.managers import PUBLISHED

from press.models import PressModel
from subscription import forms as subscription_forms

logger = logging.getLogger(__name__)

def show_home_view(request):
    language = translation.get_language()
    if language.startswith('zh'):
        language = CHINESE
    elif language.startswith('en'):
        language = ENGLISH
    elif language.startswith('ko'):
        language = KOREAN
    elif language.startswith('ja'):
        language = JAPANESE
    elif language.startswith('ru'):
        language = RUSSIAN
    elif language.startswith('tr'):
        language = TURKISH
    elif language.startswith('es'):
        language = SPANISH
    elif language.startswith('fr'):
        language = FRENCH
    elif language.startswith('de'):
        language = GERMAN
    elif language.startswith('ar'):
        language = ARABIC
    elif language.startswith('nl'):
        language = NETHERLAND
    elif language.startswith('fi'):
        language = FINNISH
    elif language.startswith('id'):
        language = INDONESIAN
    elif language.startswith('it'):
        language = ITALY
    elif language.startswith('th'):
        language = THAILAND
    else:
        language = ENGLISH
    entry = EntryDetail()
    entries = entry.get_queryset().filter(language=language, show_in_home=True, status=PUBLISHED).order_by('-creation_date')[0:3]
    if len(entries) < 3:
        entries = entry.get_queryset().filter(language=ENGLISH, show_in_home=True, status=PUBLISHED).order_by('-creation_date')[0:3]
    for entry in entries:
        if entry.entry_type == TYPE_ANNOUNCEMENT:
            url = entry.get_absolute_url().replace('/blog/', '/announcement/')
            entry.urls = url
        else:
            entry.urls = entry.get_absolute_url()
    # generate the captcha
    captcha_form = subscription_forms.SubscribeForm()
    # countdown time
    # start_day = False
    # now = datetime.datetime.now()
    # delta_time = settings.FUND_START_DATE - now
    # delta_time = delta_time.total_seconds()
    # if settings.FUND_START_DATE <= now:
    #     start_day = True
    return render(request, 'welcome/index.html', locals())

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
    return render(request, 'welcome/newpay.html', locals())

def show_community_view(request):
    presses = PressModel.objects.order_by('-created_at')[0:4]
    language = translation.get_language()
    if language.startswith('zh'):
        language = CHINESE
    elif language.startswith('en'):
        language = ENGLISH
    elif language.startswith('ko'):
        language = KOREAN
    elif language.startswith('ja'):
        language = JAPANESE
    elif language.startswith('ru'):
        language = RUSSIAN
    elif language.startswith('tr'):
        language = TURKISH
    elif language.startswith('es'):
        language = SPANISH
    elif language.startswith('fr'):
        language = FRENCH
    elif language.startswith('de'):
        language = GERMAN
    elif language.startswith('ar'):
        language = ARABIC
    elif language.startswith('nl'):
        language = NETHERLAND
    elif language.startswith('fi'):
        language = FINNISH
    elif language.startswith('id'):
        language = INDONESIAN
    elif language.startswith('it'):
        language = ITALY
    elif language.startswith('th'):
        language = THAILAND
    else:
        language = ENGLISH
    entry = EntryDetail()
    # select activity entry object
    activity_entries = entry.get_queryset().filter(language=language, status=PUBLISHED, entry_type=TYPE_ANNOUNCEMENT, entry_sub_type=0).order_by('-creation_date')[0:4]
    if len(activity_entries) < 4:
        activity_entries = entry.get_queryset().filter(language=ENGLISH, status=PUBLISHED, entry_type=TYPE_ANNOUNCEMENT, entry_sub_type=0).order_by('-creation_date')[0:4]
    # select operation entry object
    operation_entries = entry.get_queryset().filter(language=language, status=PUBLISHED, entry_type=TYPE_ANNOUNCEMENT, entry_sub_type__in=[1, 2]).order_by('-creation_date')[0:4]
    if len(operation_entries) < 4:
        operation_entries = entry.get_queryset().filter(language=ENGLISH, status=PUBLISHED, entry_type=TYPE_ANNOUNCEMENT, entry_sub_type__in=[1, 2]).order_by('-creation_date')[0:4]
    # select blog entry object
    blog_entries = entry.get_queryset().filter(language=language, status=PUBLISHED, entry_type=TYPE_BLOG).order_by('-creation_date')[0:4]
    if len(blog_entries) < 4:
        blog_entries = entry.get_queryset().filter(language=ENGLISH, status=PUBLISHED, entry_type=TYPE_BLOG).order_by('-creation_date')[0:4]
    for activity_entry in activity_entries:
        activity_entry.urls = activity_entry.get_absolute_url().replace('/blog/', '/announcement/')
    for operation_entry in operation_entries:
        operation_entry.urls = operation_entry.get_absolute_url().replace('/blog/', '/announcement/')
    for blog_entry in blog_entries:
        blog_entry.urls = blog_entry.get_absolute_url()
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

def show_addcommunity_view(request):
    return render(request, 'welcome/addcommunity.html', locals())

def show_sitemap_view(request):
    return render(request, 'welcome/sitemap.html', locals())

def show_newstatus_view(request):
    return render(request, 'welcome/newstatus.html', locals())

def show_dashboard_view(request):
    return render(request, 'welcome/dashboard.html', locals())

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
        if language.startswith('zh'):
            language = CHINESE
        elif language.startswith('en'):
            language = ENGLISH
        elif language.startswith('ko'):
            language = KOREAN
        elif language.startswith('ja'):
            language = JAPANESE
        elif language.startswith('ru'):
            language = RUSSIAN
        elif language.startswith('tr'):
            language = TURKISH
        elif language.startswith('es'):
            language = SPANISH
        elif language.startswith('fr'):
            language = FRENCH
        elif language.startswith('de'):
            language = GERMAN
        elif language.startswith('ar'):
            language = ARABIC
        elif language.startswith('nl'):
            language = NETHERLAND
        elif language.startswith('fi'):
            language = FINNISH
        elif language.startswith('id'):
            language = INDONESIAN
        elif language.startswith('it'):
            language = ITALY
        elif language.startswith('th'):
            language = THAILAND
        else:
            language = ENGLISH
            
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT,language=language, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url().replace('/blog/','/announcement/')
            entry.urls = url
        return entries

class AnnouncementSubView(generic.ListView):
    template_name = "welcome/announcement.html"
    context_object_name = "entries"
    paginate_by = 20
    
    def get_queryset(self):
        entry_sub_type = int(self.request.path.split("/")[2])
        language = translation.get_language()
        if language.startswith('zh'):
            language = CHINESE
        elif language.startswith('en'):
            language = ENGLISH
        elif language.startswith('ko'):
            language = KOREAN
        elif language.startswith('ja'):
            language = JAPANESE
        elif language.startswith('ru'):
            language = RUSSIAN
        elif language.startswith('tr'):
            language = TURKISH
        elif language.startswith('es'):
            language = SPANISH
        elif language.startswith('fr'):
            language = FRENCH
        elif language.startswith('de'):
            language = GERMAN
        elif language.startswith('ar'):
            language = ARABIC
        elif language.startswith('nl'):
            language = NETHERLAND
        elif language.startswith('fi'):
            language = FINNISH
        elif language.startswith('id'):
            language = INDONESIAN
        elif language.startswith('it'):
            language = ITALY
        elif language.startswith('th'):
            language = THAILAND
        else:
            language = ENGLISH
            
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_ANNOUNCEMENT,language=language,entry_sub_type=entry_sub_type, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url().replace('/blog/','/announcement/')
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
    