# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from config import codes

class KYCInfo(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(default='', max_length=200)
    last_name = models.CharField(default='', max_length=200)
    country = models.CharField(default='', max_length=200)
    location = models.CharField(default='', max_length=1000)
    country_code = models.CharField(max_length=4, db_index=True, default=settings.CHINA_COUNTRY_CALLING_CODE)
    cellphone = models.CharField(max_length=128, db_index=True, default='')
    email = models.EmailField()
    id_card = models.ImageField(upload_to='id_card/%Y/%m/%d/')
    investment_btc = models.FloatField()
    investment_ela = models.FloatField()
    how_to_contribute = models.TextField()
    what_is_newton = models.TextField()
    is_pass_kyc = models.BooleanField(default=False)
    btc_address = models.CharField(max_length=200, default='')
    ela_address = models.CharField(max_length=200, default='')
    btc_limit = models.FloatField()
    ela_limit = models.FloatField()
    is_has_limit = models.BooleanField(default=False)
    is_send_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    uuid = models.CharField(default='1',db_index=True, max_length="200")

