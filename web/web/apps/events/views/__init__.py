"""Views for Zinnia"""
from django.views import generic
from django.utils import translation
from django.conf import settings

from events.managers import TYPE_EVENTS
from events.managers import PUBLISHED
from events.views.entries import EntryDetail
from config import codes


class EventsView(generic.ListView):
    template_name = "welcome/events.html"
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
        entries = entry.get_queryset().filter(entry_type=TYPE_EVENTS, language=language_code, status=PUBLISHED)
        for entry in entries:
            url = entry.get_absolute_url()
            entry.urls = url
        return entries


class EventsDetailView(generic.DetailView):
    template_name = "welcome/events-detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_EVENTS)
        self.get_object(entries)
        return entries
