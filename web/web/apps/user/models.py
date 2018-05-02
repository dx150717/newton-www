# -*- coding: utf-8 -*-
import logging
import datetime
from enum import Enum
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from config import codes
from utils import storage

logger = logging.getLogger(__name__)

# Fixed: The default username length in auth user is too short
User._meta.get_field_by_name('username')[0].max_length = 128

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    user_type = models.IntegerField(default=codes.UserType.NORMAL.value)
    # cellphone
    cellphone = models.CharField(max_length=128, db_index=True, default='')
    country_code = models.CharField(max_length=4, db_index=True, default=settings.CHINA_COUNTRY_CALLING_CODE)
    language_code = models.CharField(max_length=10, default=settings.USER_DEFAULT_LANGUAGE_CODE)
    # detail
    title = models.CharField(max_length=128, default='', blank=True)
    self_introduction = models.TextField(max_length=1024, default='', blank=True, verbose_name=_('Self Introduction'))
    homepage = models.CharField(max_length=1024, default='', blank=True, verbose_name=_('Homepage'))
    head_image = models.ImageField(upload_to=storage.hashfile_upload_to('head_image', path_prefix='image'), blank=True, null=True)
    head_image_url = models.CharField(max_length=1024, blank=True, null=True)
    gender = models.IntegerField(default=codes.Gender.UNKNOWN.value, choices=settings.GENDER_LABEL, verbose_name=_('Gender'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    # geo
    country_id = models.IntegerField(default=0)
    province_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0)
    location = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('Location'))
    # verified status
    is_email_verified = models.BooleanField(default=False)
    # social
    weibo = models.CharField(max_length=1024, default='', blank=True)
    weixin = models.CharField(max_length=1024, default='', blank=True)
    qq = models.CharField(max_length=1024, default='', blank=True)
    # can sync from 3rd login
    can_sync_profile = models.BooleanField(default=True)
    # third party channel
    channel = models.CharField(max_length=128, db_index=True, blank=True, null=True, verbose_name=_('Channel'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    tall = models.IntegerField(max_length=4, null=True)
    weight = models.IntegerField(max_length=4, null=True)
    channel = models.CharField(max_length=1024,default='')
    job_status = models.IntegerField(default=codes.JobType.UNKNOWN.value, choices=settings.JOB_LABEL, verbose_name=_('Job Status'))
    major = models.CharField(default='', max_length=128, verbose_name=_('Major'))
    google_authenticator_private_key = models.CharField(default='', max_length=100)
    is_google_authenticator = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.id

    def get_first_name(self):
        return self.user.first_name
    
    def get_user_id(self):
        return self.user.id
    
    def get_username(self):
        return self.user.username
    
    def get_email(self):
        return self.user.email
    

    def get_age(self):
        now = datetime.date.today()
        age = 0
        if self.birth_date:
            age = now.year - self.birth_date.year
        return age

    def has_head_image(self):
        if self.head_image:
            return True
        return False 

    def is_active(self):
        return self.user.is_active

    def get_user_city(self):
        return self.city_id
