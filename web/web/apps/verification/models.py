# -*- coding: utf-8 -*-
from django.db import models
from config import codes
from django.utils.translation import ugettext_lazy as _

class EmailVerification(models.Model):
    """
    Entry of VerificationModel.
    """
    email_address = models.CharField(max_length=200)
    email_type = models.IntegerField() 
    uuid = models.CharField(max_length=100, unique=True)
    expire_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    def __str__(self):
        return self.email_address
    
    class Meta:
        verbose_name = _("Verification emails")
        verbose_name_plural = verbose_name
