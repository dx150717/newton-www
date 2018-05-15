# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from config import codes

class AddressTransaction(models.Model):
    user_id = models.IntegerField()
    phase_id = models.IntegerField(default=codes.FundPhase.PRIVATE.value)
    txid = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128)
    address_type = models.IntegerField()
    value = models.FloatField()
    # base fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
