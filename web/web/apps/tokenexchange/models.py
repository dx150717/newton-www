# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from utils import storage
from utils import validators
from config import codes

class KYCInfo(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=128, verbose_name='First Name')
    last_name = models.CharField(max_length=128, verbose_name='Last Name')
    cellphone = models.CharField(max_length=128, db_index=True)
    country = CountryField(blank_label="Select country or region", verbose_name='Country or Region')
    country_code = models.CharField(max_length=12, db_index=True)
    id_number = models.CharField(max_length=128, verbose_name='ID Number')
    id_card = models.FileField(upload_to=storage.hashfile_upload_to('id_card', path_prefix='id_card'), verbose_name='ID Photo', validators=[validators.validate_file_extension,validators.file_size])
    emergency_contact_first_name = models.CharField(max_length=128, verbose_name='First Name of Emergency Contact')
    emergency_contact_last_name = models.CharField(max_length=128, verbose_name='Last Name of Emergency Contact')
    emergency_contact_cellphone = models.CharField(max_length=128, db_index=True, default='', verbose_name='Cellphone of Emergency Contact')
    emergency_contact_country_code = models.CharField(max_length=4, db_index=True, verbose_name='Country Code of Emergency Contact')
    relationships_with_emergency_contacts = models.CharField(max_length=128, verbose_name='Relationships with emergency contacts')
    location = models.CharField(max_length=1024, verbose_name='Address')
    how_to_contribute = models.TextField(verbose_name='Describe yourself & how you can help as a community member', max_length=10240)
    what_is_newton = models.TextField(verbose_name='Tell us your understanding about Newton', max_length=10240)
    # base fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    class Meta:
        app_label = "tokenexchange"

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
    
    class Meta:
        app_label = "tokenexchange"

class KYCAudit(models.Model):
    user_id = models.IntegerField()
    is_pass = models.BooleanField()
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)

    class Meta:
        app_label = "tokenexchange"


class InvestInvite(models.Model):
    user_id = models.IntegerField()
    phase_id = models.IntegerField()
    round_id = models.IntegerField(default=1)
    expect_btc = models.FloatField(blank=True, null=True, verbose_name='How much do you want to contribute in BTC')
    expect_ela = models.FloatField(blank=True, null=True, verbose_name='How much do you want to contribute in ELA')
    assign_btc = models.FloatField(blank=True, null=True)
    assign_ela = models.FloatField(blank=True, null=True)
    receive_btc_address = models.CharField(max_length=128, unique=True, blank=True, null=True)
    receive_ela_address = models.CharField(max_length=128, unique=True, blank=True, null=True)
    status = models.IntegerField(default=codes.TokenExchangeStatus.INVITE.value, db_index=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = "tokenexchange"