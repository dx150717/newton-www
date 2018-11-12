# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'


from haystack import indexes
from zinnia.models.entry import Entry


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Entry

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
