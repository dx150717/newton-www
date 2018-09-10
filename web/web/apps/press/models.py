from django.db import models
from config import codes
from django.utils.translation import ugettext_lazy as _

class PressModel(models.Model):
    """
    Entry of press.
    """
    press_title = models.CharField(max_length=200)
    press_link = models.CharField(max_length=200)
    press_partner = models.CharField(max_length=200)
    press_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    press_img_url = models.CharField(max_length=200)
    
    def __str__(self):
        return self.press_title

    class Meta:
        verbose_name = _('press')
        verbose_name_plural = verbose_name
