from django.db import models

from config import codes
from django.utils.translation import ugettext_lazy as _
from zinnia.managers import CHINESE, ENGLISH

class FaqModel(models.Model):
    """
    Entry of Faq.
    """
    faq_question = models.CharField(max_length=500)
    faq_answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    LANGUAGE_CHOICES = (
        (CHINESE, "Chinese"),
        (ENGLISH, "English")
    )

    language = models.IntegerField(
        _('Language'),
        choices=LANGUAGE_CHOICES,default=CHINESE,
        db_index=True, 
        help_text=_('Language')
    )
    
    def __str__(self):
        return self.faq_question

    class Meta:
        verbose_name = _('faq')
        verbose_name_plural = verbose_name
