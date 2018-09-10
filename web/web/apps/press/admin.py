from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

class PressAdmin(admin.ModelAdmin):
    fields = ('press_title', 'press_link', 'press_summary', 'press_partner', 'press_img_url')
    list_display = ('press_title', 'press_link', 'created_at', 'press_partner', 'press_img_url')

admin.site.register(models.PressModel, PressAdmin)
