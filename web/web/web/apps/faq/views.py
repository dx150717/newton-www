from django.shortcuts import render
from django.views import generic
from . import models
from django.utils import translation
from zinnia.managers import CHINESE, ENGLISH

class FaqView(generic.ListView):

    template_name = "faq/faq.html"
    context_object_name = "faqs"
    paginate_by = 50
    
    def get_queryset(self):
        language = translation.get_language()
        if language.startswith('zh'):
            language = CHINESE
        elif language.startswith('en'):
            language = ENGLISH
        else:
            language = CHINESE
        query_set = models.FaqModel.objects.filter(language=language)

        return query_set.order_by('created_at')
