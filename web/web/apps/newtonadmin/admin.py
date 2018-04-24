from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

class NewtonAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name','country', 'location', 'country_code', 'cellphone', 'email',
        'investment_btc', 'investment_ela', 'how_to_contribute', 'what_is_newton', 'btc_address', 'ela_address',
        'btc_amount', 'ela_amount', 'pass_kyc', 'status')
    list_display = ('first_name', 'last_name', 'email', 'pass_kyc')
    search_fields = ['email']
    actions = ['send_email', 'export_cvs']

    def send_email(self, request, queryset):
        print(request)
        print(queryset[0].email)
    
    def export_cvs(self, request, queryset):
        return ""


admin.site.register(models.KycModel, NewtonAdmin)
