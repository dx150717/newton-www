# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _

from utils import storage
from config import codes

class KYCInfo(models.Model):
    user = models.ForeignKey(User)
    phase_id = models.IntegerField(default=codes.FundPhase.PRIVATE.value)
    first_name = models.CharField(max_length=200, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=200, verbose_name=_('Last Name'))
    location = models.CharField(max_length=1000, verbose_name=_('Address'))
    id_card = models.ImageField(upload_to=storage.hashfile_upload_to('id_card', path_prefix='id_card'), verbose_name=_('ID'))
    expect_btc = models.FloatField(blank=True, null=True, verbose_name=_('How much do you want to contribute in BTC'))
    expect_ela = models.FloatField(blank=True, null=True, verbose_name=_('How much do you want to contribute in ELA'))
    how_to_contribute = models.TextField(verbose_name=_('Describe yourself & how you can help as a community member'))
    what_is_newton = models.TextField(verbose_name=_('Tell us your understanding about Newton'))
    btc_address = models.CharField(max_length=200, verbose_name=_('Original Address - The BTC address you are contributing from'))
    ela_address = models.CharField(max_length=200, verbose_name=_('Original Address - The ELA address you are contributing from'))
    # receive related information
    max_btc_limit = models.FloatField(default=0)
    max_ela_limit = models.FloatField(default=0)
    min_btc_limit = models.FloatField(default=0)
    min_ela_limit = models.FloatField(default=0)
    accept_btc = models.FloatField(default=0)
    accept_ela = models.FloatField(default=0)
    receive_btc_address = models.CharField(max_length=128, unique=True, blank=True, null=True)
    receive_ela_address = models.CharField(max_length=128, unique=True, blank=True, null=True)    
    # base fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.TokenExchangeStatus.CANDIDATE.value, db_index=True)

class AddressTransaction(models.Model):
    user = models.ForeignKey(User)
    phase_id = models.IntegerField(default=codes.FundPhase.PRIVATE.value)
    txid = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128)
    address_type = models.IntegerField()    
    # base fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.TokenExchangeStatus.CANDIDATE.value, db_index=True)
    
