from django.shortcuts import render
from django.views import generic
from . import models
from django.utils import translation
from zinnia.managers import CHINESE, ENGLISH
from django.conf import settings


class FaqView(generic.ListView):

    template_name = "faq/faq.html"
    context_object_name = "faqs"
    paginate_by = 50
    
    def get_queryset(self):
        language = translation.get_language()
        language_code = ENGLISH
        for language_item in settings.LANGUAGE_LIST:
            if language.startswith(language_item[0]):
                language_code = language_item[1]
                break
        query_set = models.FaqModel.objects.filter(language=language_code)

        return query_set.order_by('created_at')
