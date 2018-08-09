from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models
from config import codes


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created_at', 'status', 'is_spam')
    actions = ['clean_emails', ]

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(SubscriptionAdmin, self).__init__(model, admin_site)

    def get_actions(self, request):
        """
        Define actions by user's permissions.
        """
        actions = super(SubscriptionAdmin, self).get_actions(request)
        return actions

    def clean_emails(self, request, queryset):
        """
        Set the entries to the current user.
        """
        for email in queryset:
            email.is_spam = codes.SubscriptionEmailType.SPAM.value
            email.save()
        self.message_user(
            request, _('Set emails as spam'))
    clean_emails.short_description = _('Set emails as spam')

admin.site.register(models.SubscribedEmail, SubscriptionAdmin)