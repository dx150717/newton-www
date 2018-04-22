# -*- coding: utf-8 -*-
import logging
import datetime
from enum import Enum
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.db.models import Q
from django.contrib.auth.models import User
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
    self_introduction = models.TextField(max_length=1024, default='', blank=True)
    homepage = models.CharField(max_length=1024, default='', blank=True)
    head_image = models.ImageField(upload_to=storage.hashfile_upload_to('head_image', path_prefix='image'), blank=True, null=True)
    head_image_url = models.CharField(max_length=1024, blank=True, null=True)
    gender = models.IntegerField(default=codes.Gender.UNKNOWN.value, choices=settings.GENDER_LABEL)
    birth_date = models.DateField(blank=True, null=True)
    # geo
    country_id = models.IntegerField(default=0)
    province_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0)
    location = models.CharField(max_length=1024, blank=True, null=True)
    # verified status
    is_email_verified = models.BooleanField(default=False)
    # social
    weibo = models.CharField(max_length=1024, default='', blank=True)
    weixin = models.CharField(max_length=1024, default='', blank=True)
    qq = models.CharField(max_length=1024, default='', blank=True)
    # can sync from 3rd login
    can_sync_profile = models.BooleanField(default=True)
    # third party channel
    channel = models.CharField(max_length=128, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
    tall = models.IntegerField(max_length=4, null=True)
    weight = models.IntegerField(max_length=4, null=True)
    newton_channel = models.IntegerField(default=0)
    job_status = models.IntegerField(default=codes.JobType.UNKNOWN.value)
    construction_mode = models.IntegerField(default=0)

    class Meta:
        unique_together = ('cellphone', 'country_code')

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
        if self.head_image and self.head_image.name != 'image/6/f/0/6f0e2562cde513f2caa97b4ffd5d4443.jpg':
            return True
        return False 

    def is_active(self):
        return self.user.is_active

    def last_login(self):
        login_user = UserLog.objects.filter(username=self.user.username).order_by("-lastlogin")
        if login_user:
            return login_user.first().lastlogin
        else:
            return None

    def get_user_city(self):
        return self.city_id


class UserConnector(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    access_token = models.CharField(max_length=1024, blank=True, null=True)
    remind_in = models.IntegerField(default=0)
    expires_in = models.DateTimeField(auto_now_add=False)
    uid = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)


def handler_fetch_3rd_profile(sender, instance, signal, *args, **kwargs):
    try:
        from user import services as user_services
        user = instance.user
        if not user.userprofile.head_image and user.userprofile.head_image_url:
            user_services.user_fetch_3rd_head_image(user)
        user_services.user_fetch_3rd_profile(user, user_from=instance.user_from)
        user_services.user_fetch_3rd_follow_list(user, user_from=instance.user_from)
        user_services.user_fetch_3rd_friend_list(user, user_from=instance.user_from)
        user_services.user_fetch_3rd_favorite_list(user, user_from=instance.user_from)
        user_services.user_fetch_3rd_post_list(user, user_from=instance.user_from)
        # todo: follow
        if settings.CAN_3RD_FOLLOW:
            user_services.user_follow_3rd_user(user, user_from=instance.user_from, uid=settings.WEIBO_UID)
        # todo: post weibo
        if settings.CAN_3RD_POST:
            user_services.user_post_3rd_weibo(user, settings.POST_CONTENT_3RD, user_from=instance.user_from)
    except Exception, inst:
        print inst
        logger.error('fail to fetch 3rd head image: %s' % str(inst))

signals.post_save.connect(handler_fetch_3rd_profile, sender=UserConnector)


class User3rdFollow(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    uid = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)


class User3rdFriend(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    uid = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)


class User3rdFavorite(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    entry_id = models.CharField(max_length=128, db_index=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)


class User3rdPost(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    entry_id = models.CharField(max_length=128, db_index=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)


class User3rdProfile(models.Model):
    user = models.ForeignKey(User)
    user_from = models.IntegerField(default=codes.UserFrom.DIRECT_REGISTER.value, db_index=True)
    gender = models.IntegerField(default=codes.Gender.MALE.value, choices=settings.GENDER_LABEL)
    # geo
    country_id = models.IntegerField(default=0)
    province_id = models.IntegerField(default=0)
    city_id = models.IntegerField(default=0)
    location = models.CharField(max_length=1024, blank=True, null=True)
    followers_count = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0),
    favourites_count = models.IntegerField(default=0)
    bi_followers_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=codes.StatusCode.AVAILABLE.value, db_index=True)
