from django.contrib import admin
from . import models

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created_at', 'status')
admin.site.register(models.SubscribedEmail, SubscriptionAdmin) 
