# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from config import codes

logger = logging.getLogger(__name__)

class AuditLog(models.Model):
    user = models.ForeignKey(User)
    target_user = models.ForeignKey(User)
    action_id = models.IntegerField()
    comment = models.CharField(max_length=200,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    