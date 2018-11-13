# -*- coding: utf-8 -*-

import logging
from haystack.query import SearchQuerySet

from django.utils import translation
from django.views import generic
from django.conf import settings

from config import codes

logger = logging.getLogger(__name__)


class IdListView(generic.ListView):
    template_name = "search/search.html"
    context_object_name = "items"
    paginate_by = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super(IdListView, self).get_context_data(**kwargs)
        context["is_idlist"] = True
        context["search_query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        try:
            language = translation.get_language()
            language_code = 1
            for language_item in settings.LANGUAGE_LIST:
                if language.startswith(language_item[0]):
                    language_code = language_item[1]
                    break
            search_query = self.request.GET.get("q")
            items = SearchQuerySet().filter(content=search_query, language=language_code).order_by("-last_update")
            return items
        except Exception, inst:
            logger.exception("fail to show id list:%s" % str(inst))
            return None
