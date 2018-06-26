# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from utils import storage
from utils import validators
from config import codes

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
LEVEL_CHOICE = [(i+1, i+1) for i in range(10)]
RELATIONSHIP_CHOICE = (
    (codes.RelationshipWithEmergency.KINSHIP.value, _('Kinship')),
    (codes.RelationshipWithEmergency.FRIENDSHIP.value, _('Friendship')),
    (codes.RelationshipWithEmergency.COLLEAGUE.value, _('Colleague')),
)

class KYCInfo(models.Model):
    user_id = models.IntegerField()
    # base info
    first_name = models.CharField(max_length=128, verbose_name=_('First Name'), help_text='*')
    last_name = models.CharField(max_length=128, verbose_name=_('Last Name'), help_text='*')
    country_code = models.CharField(max_length=4, db_index=True, help_text='*')            
    cellphone = models.CharField(max_length=20, db_index=True, verbose_name='Cellphone', help_text='*')
    country = CountryField(blank_label=_("Select country or region"), verbose_name=_('Country or Region'), help_text='*')
    city = models.CharField(max_length=256, verbose_name=_('City'), help_text='*')
    location = models.CharField(max_length=1024, verbose_name=_('Address'), help_text='*')
    id_type = models.IntegerField(
        _('ID Type'),
        choices=ID_CHOICES, default=codes.IDType.ID_CARD.value,
        db_index=True,
        help_text="*"
    )
    id_number = models.CharField(max_length=128, db_index=True, verbose_name=_('ID Number'), help_text="*")
    id_card = models.FileField(upload_to=storage.hashfile_upload_to('id_card', path_prefix='attachment'), verbose_name=_('ID Photo'), validators=[validators.validate_file_extension_of_id_photo, validators.validate_file_size_of_id_photo], help_text="*")
    
    # profile
    personal_profile = models.TextField(verbose_name=_("Self Introduction"), max_length=10240, help_text=_('(* Your CV. When were you involved in blockchain industry? Write something about your understanding on blockchain industry.)'))
    personal_profile_attachment = models.FileField(upload_to=storage.hashfile_upload_to('personal_profile_attachment', path_prefix='attachment'), verbose_name=_('Attachment'), validators=[validators.validate_file_size_of_id_photo, validators.validate_file_extension_of_id_photo])
    facebook = models.CharField(max_length=128, db_index=True, verbose_name='Facebook', null=True)
    twitter = models.CharField(max_length=128, db_index=True, verbose_name='Twitter', null=True)
    telegram = models.CharField(max_length=128, db_index=True, verbose_name='Telegram ID', null=True)
    wechat = models.CharField(max_length=128, db_index=True, verbose_name=_('WeChat ID'), null=True)
    other_social_account = models.CharField(max_length=128, db_index=True, verbose_name=_('Other Social Media'), null=True)
    your_community = models.TextField(max_length=10240, verbose_name=_('Newton Communities You are Involved in'), null=True)
    your_community_screenshots1 = models.FileField(upload_to=storage.hashfile_upload_to('your_community_screenshots1', path_prefix='attachment'), verbose_name=_('Screenshots of Abovementioned Communities 1'))
    your_community_screenshots2 = models.FileField(upload_to=storage.hashfile_upload_to('your_community_screenshots2', path_prefix='attachment'), verbose_name=_('Screenshots of Abovementioned Communities 2'))
    your_community_screenshots3 = models.FileField(upload_to=storage.hashfile_upload_to('your_community_screenshots3', path_prefix='attachment'), verbose_name=_('Screenshots of Abovementioned Communities 3'))
    # how to contribute for newton
    what_is_newton = models.TextField(verbose_name=_('Your Understanding of Newton'), max_length=10240, null=True, help_text='*')
    done_for_newton = models.TextField(verbose_name=_('Contribution You Have Made to Newton'), max_length=10240)
    done_for_newton_attachment = models.FileField(upload_to=storage.hashfile_upload_to('done_for_newton_attachment', path_prefix='attachment'), verbose_name=_("Attachment"))
    do_for_newton = models.TextField(verbose_name=_('Contribution You Will Make to Newton'), max_length=10240)
    is_establish_node = models.IntegerField(
        _('Do you want to establish a Newton node ?'),
        choices=ESTABLISH_CHOICE, default=codes.EstablishNodeType.YES.value,
        )
    which_node_establish = models.IntegerField(
            _('Which type of node ?'),
            choices=NODE_CHOICE, default=codes.NodeType.FULL_NODE.value,
        )
    establish_node_plan = models.TextField(verbose_name=_('Your plan of node establishment'))

    # emergency info
    emergency_contact_first_name = models.CharField(max_length=128, verbose_name=_('First Name'), help_text="*")
    emergency_contact_last_name = models.CharField(max_length=128, verbose_name=_('Last Name'), help_text="*")
    emergency_contact_country_code = models.CharField(max_length=4, db_index=True, verbose_name=_('Country Code of Emergency Contact'), help_text="*")
    emergency_contact_cellphone = models.CharField(max_length=20, db_index=True, default='', verbose_name=_('Cellphone of Emergency Contact'), help_text="*")
    emergency_country = CountryField(blank_label=_("Select country or region"), verbose_name=_('Country or Region'), help_text='*')
    emergency_city = models.CharField(max_length=256, verbose_name=_('City'), help_text='*')
    emergency_location = models.CharField(max_length=1024, verbose_name=_('Address'), help_text='*')
    emergency_relationship = models.IntegerField(_('Relation with Applicant'), help_text='*', choices=RELATIONSHIP_CHOICE, default=codes.RelationshipWithEmergency.KINSHIP.value, null=True)
    # level
    level = models.IntegerField(choices=LEVEL_CHOICE, default=0, db_index=True)
    # base fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    # orgnization info
    orgnization_name = models.CharField(max_length=128, verbose_name=_('Organization Name'), help_text="*")
    orgnization_code = models.CharField(max_length=128, verbose_name=_('Organization Code'), help_text="*")
    orgnization_certificate1 = models.FileField(upload_to=storage.hashfile_upload_to('orgnization_certificate1', path_prefix='attachment'), verbose_name=_('Organization Certificate'), validators=[validators.validate_file_extension_of_id_photo, validators.validate_file_size_of_id_photo], help_text="*")
    orgnization_certificate2 = models.FileField(upload_to=storage.hashfile_upload_to('orgnization_certificate2', path_prefix='attachment'), verbose_name=_('Organization Certificate'), validators=[validators.validate_file_extension_of_id_photo, validators.validate_file_size_of_id_photo])
    wechat_platform_name = models.CharField(max_length=128, db_index=True, verbose_name=_('Wechat Platform Name'), null=True)

    # kyc type
    kyc_type = models.IntegerField()
    # kyc submit type
    phase_id = models.IntegerField()

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
    expect_btc = models.FloatField(blank=True, null=True, verbose_name=_('How much do you want to contribute in BTC'))
    expect_ela = models.FloatField(blank=True, null=True, verbose_name=_('How much do you want to contribute in ELA'))
    assign_btc = models.FloatField(blank=True, null=True)
    assign_ela = models.FloatField(blank=True, null=True)
    receive_btc_address = models.CharField(max_length=128, unique=True, blank=True, null=True)
    receive_ela_address = models.CharField(max_length=128, unique=True, blank=True, null=True)
    status = models.IntegerField(default=codes.TokenExchangeStatus.INVITE.value, db_index=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # duplicate fields for backend query
    level = models.IntegerField(choices=LEVEL_CHOICE, default=1, db_index=True)
    kyc_type = models.IntegerField(default=1)
    is_establish_node = models.IntegerField(choices=ESTABLISH_CHOICE, default=codes.EstablishNodeType.NO.value)
    country = CountryField()
    class Meta:
        app_label = "tokenexchange"
