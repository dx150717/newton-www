"""Test cases for Zinnia's mixins"""
from datetime import date

from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.tests.utils import skipIfCustomUser

from events.models.entry import Entry
from events.models.author import Author
from events.models.category import Category
from events.managers import PUBLISHED
from events.tests.utils import datetime
from events.signals import disconnect_entry_signals
from events.views.mixins.archives import PreviousNextPublishedMixin
from events.views.mixins.callable_queryset import CallableQuerysetMixin
from events.views.mixins.prefetch_related import PrefetchRelatedMixin
from events.views.mixins.prefetch_related import PrefetchCategoriesAuthorsMixin
from events.views.mixins.templates import EntryQuerysetTemplateResponseMixin
from events.views.mixins.templates import EntryArchiveTemplateResponseMixin
from events.views.mixins.templates import \
    EntryQuerysetArchiveTemplateResponseMixin


class MixinTestCase(TestCase):
    """Test cases for zinnia.views.mixins"""

    def setUp(self):
        disconnect_entry_signals()

    def test_callable_queryset_mixin(self):
        instance = CallableQuerysetMixin()
        self.assertRaises(ImproperlyConfigured,
                          instance.get_queryset)

        def qs():
            return []

        instance.queryset = qs
        self.assertEqual(instance.get_queryset(),
                         [])

    def test_entry_queryset_template_response_mixin(self):
        instance = EntryQuerysetTemplateResponseMixin()
        self.assertRaises(ImproperlyConfigured,
                          instance.get_model_type)
        self.assertRaises(ImproperlyConfigured,
                          instance.get_model_name)
        instance.model_type = 'model'
        instance.model_name = 'name'
        self.assertEqual(instance.get_model_type(),
                         'model')
        self.assertEqual(instance.get_model_name(),
                         'name')
        self.assertEqual(instance.get_template_names(),
                         ['events/model/name/entry_list.html',
                          'events/model/name_entry_list.html',
                          'events/model/entry_list.html',
                          'events/entry_list.html'])
        instance.template_name = 'events/entry_search.html'
        self.assertEqual(instance.get_template_names(),
                         ['events/entry_search.html',
                          'events/model/name/entry_list.html',
                          'events/model/name_entry_list.html',
                          'events/model/entry_list.html',
                          'events/entry_list.html'])

    def test_entry_queryset_archive_template_response_mixin(self):
        get_year = lambda: 2012
        get_week = lambda: 16
        get_month = lambda: '04'
        get_day = lambda: 21
        instance = EntryQuerysetArchiveTemplateResponseMixin()
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])
        instance.get_year = get_year
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/entry_archive.html',
             'events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])
        instance.get_week = get_week
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/week/16/entry_archive.html',
             'events/archives/week/16/entry_archive.html',
             'events/archives/2012/entry_archive.html',
             'events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])
        instance.get_month = get_month
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/month/04/entry_archive.html',
             'events/archives/month/04/entry_archive.html',
             'events/archives/2012/week/16/entry_archive.html',
             'events/archives/week/16/entry_archive.html',
             'events/archives/2012/entry_archive.html',
             'events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])
        instance.get_day = get_day
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/04/21/entry_archive.html',
             'events/archives/month/04/day/21/entry_archive.html',
             'events/archives/2012/day/21/entry_archive.html',
             'events/archives/day/21/entry_archive.html',
             'events/archives/2012/month/04/entry_archive.html',
             'events/archives/month/04/entry_archive.html',
             'events/archives/2012/week/16/entry_archive.html',
             'events/archives/week/16/entry_archive.html',
             'events/archives/2012/entry_archive.html',
             'events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])

        instance.template_name = 'events/entry_search.html'
        self.assertEqual(
            instance.get_template_names(),
            ['events/entry_search.html',
             'events/archives/2012/04/21/entry_archive.html',
             'events/archives/month/04/day/21/entry_archive.html',
             'events/archives/2012/day/21/entry_archive.html',
             'events/archives/day/21/entry_archive.html',
             'events/archives/2012/month/04/entry_archive.html',
             'events/archives/month/04/entry_archive.html',
             'events/archives/2012/week/16/entry_archive.html',
             'events/archives/week/16/entry_archive.html',
             'events/archives/2012/entry_archive.html',
             'events/archives/entry_archive.html',
             'events/entry_archive.html',
             'entry_archive.html'])

    def test_entry_archive_template_response_mixin(self):
        class FakeEntry(object):
            detail_template = 'entry_detail.html'
            slug = 'my-fake-entry'

        get_year = lambda: 2012
        get_month = lambda: '04'
        get_day = lambda: 21

        instance = EntryArchiveTemplateResponseMixin()
        instance.get_year = get_year
        instance.get_month = get_month
        instance.get_day = get_day
        instance.object = FakeEntry()
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/04/21/my-fake-entry_entry_detail.html',
             'events/archives/month/04/day/21/my-fake-entry_entry_detail.html',
             'events/archives/2012/day/21/my-fake-entry_entry_detail.html',
             'events/archives/day/21/my-fake-entry_entry_detail.html',
             'events/archives/2012/04/21/my-fake-entry.html',
             'events/archives/month/04/day/21/my-fake-entry.html',
             'events/archives/2012/day/21/my-fake-entry.html',
             'events/archives/day/21/my-fake-entry.html',
             'events/archives/2012/04/21/entry_detail.html',
             'events/archives/month/04/day/21/entry_detail.html',
             'events/archives/2012/day/21/entry_detail.html',
             'events/archives/day/21/entry_detail.html',
             'events/archives/2012/month/04/my-fake-entry_entry_detail.html',
             'events/archives/month/04/my-fake-entry_entry_detail.html',
             'events/archives/2012/month/04/my-fake-entry.html',
             'events/archives/month/04/my-fake-entry.html',
             'events/archives/2012/month/04/entry_detail.html',
             'events/archives/month/04/entry_detail.html',
             'events/archives/2012/my-fake-entry_entry_detail.html',
             'events/archives/2012/my-fake-entry.html',
             'events/archives/2012/entry_detail.html',
             'events/archives/my-fake-entry_entry_detail.html',
             'events/my-fake-entry_entry_detail.html',
             'my-fake-entry_entry_detail.html',
             'events/archives/my-fake-entry.html',
             'events/my-fake-entry.html',
             'my-fake-entry.html',
             'events/archives/entry_detail.html',
             'events/entry_detail.html',
             'entry_detail.html'])

        instance.object.detail_template = 'custom.html'
        self.assertEqual(
            instance.get_template_names(),
            ['events/archives/2012/04/21/my-fake-entry_custom.html',
             'events/archives/month/04/day/21/my-fake-entry_custom.html',
             'events/archives/2012/day/21/my-fake-entry_custom.html',
             'events/archives/day/21/my-fake-entry_custom.html',
             'events/archives/2012/04/21/my-fake-entry.html',
             'events/archives/month/04/day/21/my-fake-entry.html',
             'events/archives/2012/day/21/my-fake-entry.html',
             'events/archives/day/21/my-fake-entry.html',
             'events/archives/2012/04/21/custom.html',
             'events/archives/month/04/day/21/custom.html',
             'events/archives/2012/day/21/custom.html',
             'events/archives/day/21/custom.html',
             'events/archives/2012/month/04/my-fake-entry_custom.html',
             'events/archives/month/04/my-fake-entry_custom.html',
             'events/archives/2012/month/04/my-fake-entry.html',
             'events/archives/month/04/my-fake-entry.html',
             'events/archives/2012/month/04/custom.html',
             'events/archives/month/04/custom.html',
             'events/archives/2012/my-fake-entry_custom.html',
             'events/archives/2012/my-fake-entry.html',
             'events/archives/2012/custom.html',
             'events/archives/my-fake-entry_custom.html',
             'events/my-fake-entry_custom.html',
             'my-fake-entry_custom.html',
             'events/archives/my-fake-entry.html',
             'events/my-fake-entry.html',
             'my-fake-entry.html',
             'events/archives/custom.html',
             'events/custom.html',
             'custom.html'])

    def test_previous_next_published_mixin(self):
        site = Site.objects.get_current()

        params = {'title': 'Entry 1', 'content': 'Entry 1',
                  'slug': 'entry-1', 'status': PUBLISHED,
                  'creation_date': datetime(2012, 1, 1, 12)}
        entry_1 = Entry.objects.create(**params)
        entry_1.sites.add(site)

        params = {'title': 'Entry 2', 'content': 'Entry 2',
                  'slug': 'entry-2', 'status': PUBLISHED,
                  'creation_date': datetime(2012, 3, 15, 12)}
        entry_2 = Entry.objects.create(**params)
        entry_2.sites.add(site)

        params = {'title': 'Entry 3', 'content': 'Entry 3',
                  'slug': 'entry-3', 'status': PUBLISHED,
                  'creation_date': datetime(2013, 6, 2, 12)}
        entry_3 = Entry.objects.create(**params)
        entry_3.sites.add(site)

        class EntryPreviousNextPublished(PreviousNextPublishedMixin):
            def get_queryset(self):
                return Entry.published.all()

        test_date = datetime(2009, 12, 1)
        epnp = EntryPreviousNextPublished()
        self.assertEqual(epnp.get_previous_year(test_date), None)
        self.assertEqual(epnp.get_previous_week(test_date), None)
        self.assertEqual(epnp.get_previous_month(test_date), None)
        self.assertEqual(epnp.get_previous_day(test_date), None)
        self.assertEqual(epnp.get_next_year(test_date), date(2012, 1, 1))
        self.assertEqual(epnp.get_next_week(test_date), date(2011, 12, 26))
        self.assertEqual(epnp.get_next_month(test_date), date(2012, 1, 1))
        self.assertEqual(epnp.get_next_day(test_date), date(2012, 1, 1))

        test_date = datetime(2012, 1, 1)
        epnp = EntryPreviousNextPublished()
        self.assertEqual(epnp.get_previous_year(test_date), None)
        self.assertEqual(epnp.get_previous_week(test_date), None)
        self.assertEqual(epnp.get_previous_month(test_date), None)
        self.assertEqual(epnp.get_previous_day(test_date), None)
        self.assertEqual(epnp.get_next_year(test_date), date(2013, 1, 1))
        self.assertEqual(epnp.get_next_week(test_date), date(2012, 3, 12))
        self.assertEqual(epnp.get_next_month(test_date), date(2012, 3, 1))
        self.assertEqual(epnp.get_next_day(test_date), date(2012, 3, 15))

        test_date = datetime(2012, 3, 15)
        epnp = EntryPreviousNextPublished()
        self.assertEqual(epnp.get_previous_year(test_date), None)
        self.assertEqual(epnp.get_previous_week(test_date), date(2011, 12, 26))
        self.assertEqual(epnp.get_previous_month(test_date), date(2012, 1, 1))
        self.assertEqual(epnp.get_previous_day(test_date), date(2012, 1, 1))
        self.assertEqual(epnp.get_next_year(test_date), date(2013, 1, 1))
        self.assertEqual(epnp.get_next_week(test_date), date(2013, 5, 27))
        self.assertEqual(epnp.get_next_month(test_date), date(2013, 6, 1))
        self.assertEqual(epnp.get_next_day(test_date), date(2013, 6, 2))

        test_date = datetime(2013, 6, 2)
        epnp = EntryPreviousNextPublished()
        self.assertEqual(epnp.get_previous_year(test_date), date(2012, 1, 1))
        self.assertEqual(epnp.get_previous_week(test_date), date(2012, 3, 12))
        self.assertEqual(epnp.get_previous_month(test_date), date(2012, 3, 1))
        self.assertEqual(epnp.get_previous_day(test_date), date(2012, 3, 15))
        self.assertEqual(epnp.get_next_year(test_date), None)
        self.assertEqual(epnp.get_next_week(test_date), None)
        self.assertEqual(epnp.get_next_month(test_date), None)
        self.assertEqual(epnp.get_next_day(test_date), None)

        test_date = datetime(2014, 5, 1)
        epnp = EntryPreviousNextPublished()
        self.assertEqual(epnp.get_previous_year(test_date), date(2013, 1, 1))
        self.assertEqual(epnp.get_previous_week(test_date), date(2013, 5, 27))
        self.assertEqual(epnp.get_previous_month(test_date), date(2013, 6, 1))
        self.assertEqual(epnp.get_previous_day(test_date), date(2013, 6, 2))
        self.assertEqual(epnp.get_next_year(test_date), None)
        self.assertEqual(epnp.get_next_week(test_date), None)
        self.assertEqual(epnp.get_next_month(test_date), None)
        self.assertEqual(epnp.get_next_day(test_date), None)

    def test_prefetch_related_mixin(self):
        instance = PrefetchRelatedMixin()
        self.assertRaises(ImproperlyConfigured,
                          instance.get_queryset)
        instance.relation_names = 'string'
        self.assertRaises(ImproperlyConfigured,
                          instance.get_queryset)

    @skipIfCustomUser
    def test_prefetch_categories_authors_mixin(self):
        author = Author.objects.create_user(username='author',
                                            email='author@example.com')
        category = Category.objects.create(title='Category',
                                           slug='category')
        for i in range(3):
            params = {'title': 'My entry',
                      'content': 'My content',
                      'slug': 'my-entry-%s' % i}
            entry = Entry.objects.create(**params)
            entry.authors.add(author)
            entry.categories.add(category)

        class View(object):
            def get_queryset(self):
                return Entry.objects.all()

        class ViewCategoriesAuthorsPrefetched(
                PrefetchCategoriesAuthorsMixin, View):
            pass

        with self.assertNumQueries(7):
            for entry in View().get_queryset():
                entry.authors.count()
                entry.categories.count()

        with self.assertNumQueries(3):
            for entry in ViewCategoriesAuthorsPrefetched().get_queryset():
                entry.authors.count()
                entry.categories.count()
