"""Views for Zinnia entries"""
from django.views.generic.dates import BaseDateDetailView

from events.models.entry import Entry
from events.views.mixins.archives import ArchiveMixin
from events.views.mixins.entry_preview import EntryPreviewMixin
from events.views.mixins.entry_protection import EntryProtectionMixin
from events.views.mixins.callable_queryset import CallableQuerysetMixin
from events.views.mixins.templates import EntryArchiveTemplateResponseMixin


class EntryDateDetail(ArchiveMixin,
                      EntryArchiveTemplateResponseMixin,
                      CallableQuerysetMixin,
                      BaseDateDetailView):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views
    - EntryArchiveTemplateResponseMixin to provide a
      custom templates depending on the date
    - BaseDateDetailView to retrieve the entry with date and slug
    - CallableQueryMixin to defer the execution of the *queryset*
      property when imported
    """
    queryset = Entry.published.on_site


class EntryDetail(EntryPreviewMixin,
                  EntryProtectionMixin,
                  EntryDateDetail):
    """
    Detailled archive view for an Entry with password
    and login protections and restricted preview.
    """
