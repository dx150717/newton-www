"""Managers of Zinnia"""
from django.db import models
from django.utils import timezone
from django.contrib.sites.models import Site
from django.utils import translation
from django.conf import settings

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2

CHINESE = 0
ENGLISH = 1
KOREAN = 2
JAPANESE = 3
RUSSIAN = 4
TURKISH = 5
SPANISH = 6
FRENCH = 7
GERMAN = 8
ARABIC = 9
NETHERLAND = 10
FINNISH = 11
INDONESIAN = 12
ITALY = 13
THAILAND = 14
PORTUGUESE = 15
VIETNAMESE = 16
ROMANIA = 17

TYPE_BLOG = 0
TYPE_ANNOUNCEMENT = 1
TYPE_COMMUNITY_VOICE = 2

SUB_TYPE_ACTIVITY = 0
SUB_TYPE_OPERATION = 1
SUB_TYPE_WEEKLY = 2

def tags_published():
    """
    Return the published tags.
    """
    from tagging.models import Tag
    from zinnia.models.entry import Entry
    tags_entry_published = Tag.objects.usage_for_queryset(
        Entry.published.all())
    # Need to do that until the issue #44 of django-tagging is fixed
    return Tag.objects.filter(name__in=[t.name for t in tags_entry_published])


def entries_published(queryset):
    """
    Return only the entries published.
    """
    now = timezone.now()
    language = translation.get_language()
    language_code = ENGLISH
    for language_item in settings.LANGUAGE_LIST:
        if language.startswith(language_item[0]):
            language_code = language_item[1]
            break
        
    return queryset.filter(
        models.Q(start_publication__lte=now) |
        models.Q(start_publication=None),
        models.Q(end_publication__gt=now) |
        models.Q(end_publication=None),
        status=PUBLISHED, sites=Site.objects.get_current(), language=language_code, entry_type=TYPE_BLOG)

class EntryPublishedManager(models.Manager):
    """
    Manager to retrieve published entries.
    """

    def get_queryset(self):
        """
        Return published entries.
        """
        return entries_published((super(EntryPublishedManager, self).get_queryset()))

    def on_site(self):
        """
        Return entries published on current site.
        """
        return super(EntryPublishedManager, self).get_queryset().filter(
            sites=Site.objects.get_current())

    def search(self, pattern):
        """
        Top level search method on entries.
        """
        try:
            return self.advanced_search(pattern)
        except:
            return self.basic_search(pattern)

    def advanced_search(self, pattern):
        """
        Advanced search on entries.
        """
        from zinnia.search import advanced_search
        return advanced_search(pattern)

    def basic_search(self, pattern):
        """
        Basic search on entries.
        """
        lookup = None
        for pattern in pattern.split():
            query_part = models.Q(content__icontains=pattern) | \
                models.Q(excerpt__icontains=pattern) | \
                models.Q(title__icontains=pattern)
            if lookup is None:
                lookup = query_part
            else:
                lookup |= query_part

        return self.get_queryset().filter(lookup)


class EntryRelatedPublishedManager(models.Manager):
    """
    Manager to retrieve objects associated with published entries.
    """

    def get_queryset(self):
        """
        Return a queryset containing published entries.
        """
        now = timezone.now()
        return super(
            EntryRelatedPublishedManager, self).get_queryset().filter(
            models.Q(entries__start_publication__lte=now) |
            models.Q(entries__start_publication=None),
            models.Q(entries__end_publication__gt=now) |
            models.Q(entries__end_publication=None),
            entries__status=PUBLISHED,
            entries__sites=Site.objects.get_current()
            ).distinct()
