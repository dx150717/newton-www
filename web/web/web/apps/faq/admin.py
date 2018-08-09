from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

class FaqAdmin(admin.ModelAdmin):
    fields = ('faq_question', 'faq_answer','language')
    list_display = ('faq_question',)
    search_fields = ['faq_question']

admin.site.register(models.FaqModel, FaqAdmin)
