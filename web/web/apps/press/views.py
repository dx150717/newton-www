from django.shortcuts import render
from django.views import generic
from . import models

class PressView(generic.ListView):

    template_name = "welcome/press.html"
    context_object_name = "presses"
    paginate_by = 20
    
    def get_queryset(self):
        return models.PressModel.objects.order_by('-created_at')
