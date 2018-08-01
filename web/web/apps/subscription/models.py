from django.db import models
from config import codes
from django.utils.translation import ugettext_lazy as _

class SubscribedEmail(models.Model):
    """
    Entry of Subscribed Email. And we can get subscribed email list.
    """
    email_address = models.CharField(max_length=200, db_index=True)
    uuid = models.CharField(max_length=200, null=False)
    is_spam = models.IntegerField(db_index=True, default=codes.SubscriptionEmailType.AVAILABLE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    def __str__(self):
        return self.email_address
    
    class Meta:
        verbose_name = _("Subscribed emails")
        verbose_name_plural = verbose_name
