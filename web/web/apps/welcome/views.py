# -*- coding: utf-8 -*-
__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """  """

import json
import random
import time

from django.views import generic
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.utils import translation
from zinnia.views.entries import EntryDetail
from zinnia.managers import CHINESE,ENGLISH,TYPE_BLOG,TYPE_ANNOUNCEMENT,KOREAN,JAPANESE,RUSSIAN,TURKISH,SPANISH,FRENCH,GERMAN,ARABIC,NETHERLAND
from zinnia.managers import PUBLISHED

from press.models import PressModel
from subscription import forms as subscription_forms


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
    else:
        language = ENGLISH
    entry = EntryDetail()
    entries = entry.get_queryset().filter(language=language, show_in_home=True, status=PUBLISHED).order_by('-creation_date')[0:5]
    for entry in entries:
        if entry.entry_type == TYPE_ANNOUNCEMENT:
            url = entry.get_absolute_url().replace('/blog/','/announcement/')
            entry.urls = url
        else:
            entry.urls = entry.get_absolute_url()
    # generate the captcha
    captcha_form = subscription_forms.SubscribeForm()

    return render(request, 'welcome/index.html', locals())

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
    presses = PressModel.objects.order_by('-created_at')[0:5]
    return render(request, 'welcome/community.html', locals())

def show_economy_view(request):
    return render(request, 'welcome/economy.html', locals())

def show_whitepaper_view(request):
    return render(request, 'welcome/whitepaper.html', locals())
        
def show_wechat_view(request):
    return render(request, 'welcome/wechat.html', locals())

def show_foundation_view(request):
    return render(request, 'welcome/foundation.html', locals())

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
    