"""Views for Zinnia"""

import logging
import datetime

from django.views import generic
from django.utils import translation
from django.conf import settings
from django.db.models import Q

from events.managers import TYPE_EVENTS
from events.managers import PUBLISHED
from events.views.entries import EntryDetail
from config import codes
from utils import http

logger = logging.getLogger(__name__)


class EventsView(generic.ListView):
    template_name = "welcome/events.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        entries = context["entries"]
        coming_entries = []
        passed_entries = []
        for item in entries:
            if item.event_date >= datetime.date.today():
                coming_entries.append(item)
            else:
                passed_entries.append(item)
        context["coming_entries"] = coming_entries[::-1]
        context["passed_entries"] = passed_entries
        return context

    def get_queryset(self):
        language = translation.get_language()
        language_code = codes.EntryLanguage.ENGLISH.value
        q = Q(entry_type=TYPE_EVENTS, status=PUBLISHED)
        event_date = self.request.GET.get("event_date")
        if event_date:
            q &= Q(event_date=event_date)
        for language_item in settings.LANGUAGE_LIST:
            if language.startswith(language_item[0]):
                language_code = language_item[1]
                break
        entry = EntryDetail()
        entries = entry.get_queryset().filter(q).filter(language=language_code).order_by("-event_date")
        if not entries:
            entries = entry.get_queryset().filter(q).filter(language=codes.EntryLanguage.ENGLISH.value,).order_by("-event_date")
        for entry in entries:
            url = entry.get_absolute_url()
            if entry.event_link:
                url = entry.event_link
            elif not entry.content:
                url = None
            if url:
                entry.urls = url
        return entries


class EventsDetailView(generic.DetailView):
    template_name = "welcome/events-detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        kwargs = self.request.resolver_match.kwargs
        event_year = int(kwargs.get("year"))
        event_month = int(kwargs.get("month"))
        event_day = int(kwargs.get("day"))
        event_slug = kwargs.get("slug")
        start_date = datetime.date(event_year, event_month, event_day)
        end_date = start_date + datetime.timedelta(days=1)
        entry = EntryDetail()
        entries = entry.get_queryset().filter(entry_type=TYPE_EVENTS,
                                              slug=event_slug,
                                              creation_date__gte=start_date,
                                              creation_date__lt=end_date)
        return entries


def get_events_date(request):
    """
    Get all events date for events calendar request
    :param request:
    :return: JsonResponse
    """
    try:
        entry = EntryDetail()
        entries_date = entry.get_queryset().filter(entry_type=TYPE_EVENTS).dates("event_date", "day")
        result = []
        for entry_date in entries_date:
            event_data = {}
            event_data["start"] = str(entry_date)
            event_data["url"] = "?event_date=%s" % str(entry_date)
            result.append(event_data)
        return http.JsonSuccessResponse(data=result)
    except Exception, inst:
        logger.exception("fail to get events date: %s" % str(inst))
        return http.JsonErrorResponse()
