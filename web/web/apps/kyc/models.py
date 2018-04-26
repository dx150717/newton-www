# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from utils import storage
from config import codes

class KYCInfo(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    location = models.CharField(max_length=1000)
    country_code = models.CharField(max_length=4, db_index=True)
    cellphone = models.CharField(max_length=128, db_index=True)
    email = models.EmailField()
    id_card = models.ImageField(upload_to=storage.hashfile_upload_to('id_card', path_prefix='idcard'), blank=True, null=True)
    expect_btc = models.FloatField(default=0)
    expect_ela = models.FloatField(default=0)
    how_to_contribute = models.TextField()
    what_is_newton = models.TextField()
    btc_address = models.CharField(max_length=200)
    ela_address = models.CharField(max_length=200)
    max_btc_limit = models.FloatField(default=0)
    max_ela_limit = models.FloatField(default=0)
    min_btc_limit = models.FloatField(default=0)
    min_ela_limit = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

