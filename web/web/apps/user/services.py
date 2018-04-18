# -*- coding: utf-8 -*-
import datetime

__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """   """


import logging
import os
from django.conf import settings
from config import codes
from filestorage import services as filestorage_services
from utils import crawler
from utils import security
from utils import misc
from utils.connect import sina_weibo
from utils.connect import qq
from user import models as user_models

logger = logging.getLogger(__name__)

def user_fetch_3rd_head_image(user):
    """
    user_fetch_3rd_head_image: fetch the user head image for 3rd login
    """
    try:
        url = user.userprofile.head_image_url
        if url:
            content = crawler.fetch_file(url)
            if content:
                filename = "%s/%s" % (settings.TMP_PATH, security.generate_uuid())
                f = open(filename, 'w+')
                f.write(content)
                f.close()
                final_filename = filestorage_services.filestorage_add_image(filename)
                user.userprofile.head_image = final_filename
                user.userprofile.save()
    except Exception, inst:
        logger.error('fail to fetch 3rd head image: %s' % str(inst))
        
def user_fetch_3rd_profile(user, user_from=None):
    """
    user_fetch_3rd_profile: fetch the profile from 3rd union login
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            response = client.users.show.get(uid=user_connector.uid)
            result = user_models.User3rdProfile.objects.filter(user=user, user_from=user_from)
            if result.count() == 0:
                user_3rd_profile = user_models.User3rdProfile()
                user_3rd_profile.user = user
            else:
                user_3rd_profile = result[0]
            # gender
            if response.gender == 'm':
                user_3rd_profile.gender = codes.Gender.MALE.value
            elif response.gender == 'f':
                user_3rd_profile.gender = codes.Gender.FEMALE.value
            else:
                user_3rd_profile.gender = codes.Gender.UNKNOWN.value
            # country
            user_3rd_profile.province_id = response.province
            user_3rd_profile.city_id = response.city
            user_3rd_profile.location = response.location
            user_3rd_profile.followers_count = response.followers_count
            user_3rd_profile.friends_count = response.friends_count
            user_3rd_profile.statuses_count = response.statuses_count
            user_3rd_profile.favourites_count = response.favourites_count
            user_3rd_profile.bi_followers_count = response.bi_followers_count
            user_3rd_profile.verified = response.verified
            # store other data
            user_3rd_profile.content = str(response)
            user_3rd_profile.save()
            # set current profile
            if user.can_sync_profile:
                user.userprofile.province_id = user_3rd_profile.province_id
                user.userprofile.city_id = user_3rd_profile.city_id
                user.userprofile.location = user_3rd_profile.location
                user.userprofile.gender = user_3rd_profile.gender
                user.userprofile.save()
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        print inst
        logger.error('fail to fetch 3rd profile: %s' % str(inst))

def user_post_3rd_weibo(user, content, user_from=None):
    """
    user_post_3rd_weibo: post ad weibo
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]

        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            response = client.statuses.update.post(status=content)
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to post 3rd weibo: %s' % str(inst))

def user_follow_3rd_user(user, user_from, uid):
    """
    user_follow_3rd_user: follow 3rd user
    """
    try:
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            response = client.friendships.create.post(uid=uid)
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to follow 3rd user: %s' % str(inst))

def user_fetch_3rd_follow_list(user, user_from=None):
    """
    user_fetch_3rd_follow_list: Fetch the follow list for 3rd login user
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            uids = []
            page_size = 50
            response = client.friendships.friends.ids.get(count=page_size)
            total_number = response.total_number
            total_page = misc.get_total_page(total_number, page_size)
            uids.extend(response.ids)
            if total_page > 1:
                page_id = 2
                while page_id <= total_page:
                    response = client.friendships.friends.ids.get(count=page_size, page=page_id)
                    uids.extend(response.ids)
                    page_id += 1
            for uid in uids:
                if user_models.User3rdFollow.objects.filter(user=user, uid=uid).count() == 0:
                    follow = user_models.User3rdFollow()
                    follow.user = user
                    follow.uid = uid
                    follow.save()
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to fetch 3rd follow list: %s' % str(inst))

def user_fetch_3rd_friend_list(user, user_from=None):
    """
    user_fetch_3rd_friend_list: Fetch the friend list for 3rd login user
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            uids = []
            page_size = 50
            response = client.friendships.friends.bilateral.ids.get(count=page_size)
            total_number = response.total_number
            total_page = misc.get_total_page(total_number, page_size)
            uids.extend(response.ids)
            if total_page > 1:
                page_id = 2
                while page_id <= total_page:
                    response = client.friendships.friends.bilateral.ids.get(count=page_size, page=page_id)
                    uids.extend(response.ids)
                    page_id += 1
            for uid in uids:
                if user_models.User3rdFriend.objects.filter(user=user, uid=uid).count() == 0:
                    friend = user_models.User3rdFriend()
                    friend.user = user
                    friend.uid = uid
                    friend.save()
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to fetch 3rd friend list: %s' % str(inst))

def user_fetch_3rd_favorite_list(user, user_from=None):
    """
    user_fetch_3rd_favorite_list: Fetch the favorite list for 3rd login user
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            favorites = []
            page_size = 50
            response = client.favorites.get(count=page_size)
            total_number = response.total_number
            total_page = misc.get_total_page(total_number, page_size)
            favorites.extend(response.favorites)
            if total_page > 1:
                page_id = 2
                while page_id <= total_page:
                    response = client.favorites.get(count=page_size, page=page_id)
                    favorites.extend(response.favorites)
                    page_id += 1
            for favorite in favorites:
                if user_models.User3rdFavorite.objects.filter(user=user, entry_id=favorite.status.id).count() == 0:
                    favorite_instance = user_models.User3rdFavorite()
                    favorite_instance.user = user
                    favorite_instance.entry_id = favorite.status.id
                    favorite_instance.content = str(favorite)
                    favorite_instance.save()
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to fetch 3rd favorite list: %s' % str(inst))

def user_fetch_3rd_post_list(user, user_from=None):
    """
    user_fetch_3rd_post_list: Fetch the post list for 3rd login user
    """
    try:
        if not user_from:
            user_from = user.userprofile.user_from
        # Get the latest union login info
        result = user_models.UserConnector.objects.filter(user=user, user_from=user_from, status=codes.StatusCode.AVAILABLE.value).order_by('-created_at')
        if result.count() == 0:
            return False
        user_connector = result[0]
        if user_from == codes.UserFrom.WEIBO.value:
            client = sina_weibo.APIClient(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, settings.WEIBO_CALLBACK_URL)
            client.set_access_token(user_connector.access_token, user_connector.expires_in)
            posts = []
            page_size = 50
            response = client.statuses.user_timeline.get(count=page_size)
            total_number = response.total_number
            total_page = misc.get_total_page(total_number, page_size)
            posts.extend(response.statuses)
            if total_page > 1:
                page_id = 2
                while page_id <= total_page:
                    response = client.statuses.user_timeline.get(count=page_size, page=page_id)
                    posts.extend(response.statuses)
                    page_id += 1
            for post in posts:
                if user_models.User3rdFavorite.objects.filter(user=user, entry_id=post.id).count() == 0:
                    post_instance = user_models.User3rdPost()
                    post_instance.user = user
                    post_instance.entry_id = post.id
                    post_instance.content = str(post)
                    post_instance.save()
        elif user_from == codes.UserFrom.QQ.value:
            client = qq.OauthClient(app_key=settings.QQ_API_KEY, app_secret=settings.QQ_API_SECRET, app_callback=settings.QQ_CALLBACK_URL)
        else:
            pass
    except Exception, inst:
        logger.error('fail to fetch 3rd post list: %s' % str(inst))

def get_user_diamonds(user_id):
    try:
        return user_models.UserProfile.objects.get(user__id=user_id).diamonds
    except Exception, inst:
        logger.exception('fail to get user diamonds:%s' % str(inst))
    else:
        return 0

def get_user_coins(user_id):
    try:
        return user_models.UserProfile.objects.get(user__id=user_id).coins
    except Exception, inst:
        logger.exception('fail to get user coins:%s' % str(inst))
    else:
        return 0

def create_user_by_admin(cellphone, password, first_name, country_code=settings.CHINA_COUNTRY_CALLING_CODE, coins=0, diamonds=0):
    """
    create_user_by_admin: create user by admin user
    """
    try:
        if user_models.UserProfile.objects.filter(country_code=country_code, cellphone=cellphone, user_type=codes.UserType.PERSONAL.value).count() > 0:
            return False
        username = security.generate_uuid()
        user = user_models.User.objects.create_user(username, password=password, first_name=first_name)
        user_profile = user_models.UserProfile.objects.create(user=user, user_type=codes.UserType.PERSONAL.value)
        user_profile.cellphone = cellphone
        user_profile.country_code = country_code
        user_profile.coins = coins
        user_profile.diamonds = diamonds
        user_profile.save()
        return True
    except Exception, inst:
        logger.exception('fail to create user by admin:%s' % str(inst))
        return False
    
def create_admin_user(email, password):
    """
    create_admin_user: create admin user by given email
    """
    try:
        username = security.generate_uuid()
        user = user_models.User.objects.db_manager(settings.ADMIN_DB_ALIAS).create_user(username, password=password, first_name=email, email=email)
        return True
    except Exception, inst:
        logger.exception('fail to create admin user:%s' % str(inst))
        return False
