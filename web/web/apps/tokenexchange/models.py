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
    ID_CHOICES = (
        (codes.IDType.ID_CARD.value, _('ID Card')),
        (codes.IDType.PASSPORT.value, _('Passport')),
        (codes.IDType.DRIVERS_LICENSE.value, _('Drivers License'))
    )
    NODE_CHOICE = (
        (codes.NodeType.FULL_NODE.value, _('Full Node')),
        (codes.NodeType.MEDIA_NODE.value, _('Media Node')),
        (codes.NodeType.TECH_NODE.value, _('Technology Node')),
        (codes.NodeType.OPERATION_NODE.value, _('Operation Node'))
    )
    ESTABLISH_CHOICE = (
        (codes.EstablishNodeType.YES.value, _('Yes')),
        (codes.EstablishNodeType.NO.value, _('No'))
    )

    user_id = models.IntegerField()
    # base info
    first_name = models.CharField(max_length=128, verbose_name='First Name', help_text='(*)')
    last_name = models.CharField(max_length=128, verbose_name='Last Name', help_text='(*)')
    country_code = models.CharField(max_length=4, db_index=True, help_text='(*)')            
    cellphone = models.CharField(max_length=20, db_index=True, verbose_name='Cellphone', help_text='(*)')
    country = CountryField(blank_label="Select country or region", verbose_name='Country or Region', help_text='(*)')
    city = models.CharField(max_length=256, verbose_name='City', help_text='(*)')
    location = models.CharField(max_length=1024, verbose_name='Address', help_text='(*)')
    id_type = models.IntegerField(
        _('ID Type'),
        choices=ID_CHOICES, default=codes.IDType.ID_CARD.value,
        db_index=True,
        help_text="(*)"
    )
    id_number = models.CharField(max_length=128, db_index=True, verbose_name='ID Number', help_text="(*)")
    id_card = models.FileField(upload_to=storage.hashfile_upload_to('id_card', path_prefix='id_card'), verbose_name='ID Photo', validators=[validators.validate_file_extension_of_id_photo, validators.validate_file_size_of_id_photo], help_text="(*)")
    
    # profile
    personal_profile = models.TextField(verbose_name="Self Introduction", max_length=10240, help_text="(*)")
    personal_profile_attachment = models.FileField(upload_to=storage.hashfile_upload_to('personal_profile_attachment', path_prefix='personal_profile_attachment'), verbose_name='Attachment', validators=[validators.validate_file_size_of_id_photo, validators.validate_file_extension_of_id_photo])
    facebook = models.CharField(max_length=128, db_index=True, verbose_name='Facebook', null=True)
    twitter = models.CharField(max_length=128, db_index=True, verbose_name='Twitter', null=True)
    telegram = models.CharField(max_length=128, db_index=True, verbose_name='Telegram ID', null=True)
    wechat = models.CharField(max_length=128, db_index=True, verbose_name='WeChat ID', null=True)
    other_social_account = models.CharField(max_length=128, db_index=True, verbose_name='Other Social Media', null=True)
    your_community = models.CharField(max_length=1024, verbose_name='Newton Communities You are Involved in', null=True)
    your_community_screenshots = models.FileField(upload_to=storage.hashfile_upload_to('your_community_screenshots', path_prefix='your_community_screenshots'), verbose_name='Screenshots of Abovementioned Communities')

    # how to contribute for newton
    what_is_newton = models.TextField(verbose_name='Tell us your understanding about Newton', max_length=10240, null=True, help_text='(*)')
    done_for_newton = models.TextField(verbose_name='What contribute you had do for newton', max_length=10240)
    done_for_newton_attachment = models.FileField(upload_to=storage.hashfile_upload_to('done_for_newton_attachment', path_prefix='done_for_newton_attachment'), verbose_name="Attachment")
    do_for_newton = models.TextField(verbose_name='What will you do for newton', max_length=10240)
    is_establish_node = models.IntegerField(
        _('Do you want to establish a Newton node ?'),
        choices=ESTABLISH_CHOICE, default=codes.EstablishNodeType.YES.value,
        )
    which_node_establish = models.IntegerField(
            _('Which type of node ?'),
            choices=NODE_CHOICE, default=codes.NodeType.FULL_NODE.value,
        )
    establish_node_plan = models.TextField(verbose_name='Your plan of node establishment')

    # emergency info
    emergency_contact_first_name = models.CharField(max_length=128, verbose_name='First Name of Emergency Contact', help_text="(*)")
    emergency_contact_last_name = models.CharField(max_length=128, verbose_name='Last Name of Emergency Contact', help_text="(*)")
    emergency_contact_country_code = models.CharField(max_length=4, db_index=True, verbose_name='Country Code of Emergency Contact', help_text="(*)")
    emergency_contact_cellphone = models.CharField(max_length=20, db_index=True, default='', verbose_name='Cellphone of Emergency Contact', help_text="(*)")
    emergency_country = CountryField(blank_label="Select country or region", verbose_name='Emergency Country or Region', help_text='(*)')
    emergency_city = models.CharField(max_length=256, verbose_name='City', help_text='(*)')
    emergency_location = models.CharField(max_length=1024, verbose_name='Emergency Location', help_text='(*)')
    emergency_relationship = models.CharField(max_length=1024, verbose_name='Emergency Relationship', help_text='(*)')

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
