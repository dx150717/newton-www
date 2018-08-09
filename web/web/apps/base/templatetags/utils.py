# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """ """

import logging
import re
import datetime
from django import template
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext
from django.utils.translation import ungettext as _
from sorl.thumbnail import get_thumbnail
from django.utils.safestring import mark_safe
from django.utils.timezone import utc
from django_countries.data import COUNTRIES

from config import codes
from django.utils import translation

logger = logging.getLogger(__name__)

register = template.Library()
version_pattern = re.compile(r"^(.*)\.(.*?)$")


def version(path_string):
    """
    version: show the absolute url including version number
    """
    try:
        return "%s%s?v=%s" % (settings.STATIC_URL, path_string, settings.STATIC_DEFAULT_VERSION)
    except Exception, inst:
        logger.exception(str(inst))
        return path_string


register.simple_tag(version)


def menu_active(uri, key):
    if uri.find(key) >= 0:
        return "active"
    return ""


register.filter(menu_active)


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css, "placeholder": field.label})


@register.filter(name='get_head_url')
def get_head_url(user):
    if hasattr(user, 'userprofile') and user.userprofile:
        if user.userprofile.head_image:
            return '/filestorage/%s' % user.userprofile.head_image
        elif user.userprofile.head_image_url:
            return user.userprofile.head_image_url
    return '/static/images/user.jpg'


@register.filter(name='show_star_title')
def show_star_title(score):
    for key, label in settings.RANK_TYPE_LABEL:
        if key == score:
            return label
    return ''


@register.filter(name='duration_format')
def duration_format(duration):
    if duration > 0:
        if duration < 60:
            return _('%(duration)d minute', '%(duration)d minutes', duration) % {'duration': duration}
        else:
            return _('%(duration)d hour', '%(duration)d hours', duration / 60) % {'duration': duration / 60}
    return ''


@register.simple_tag()
def multiply(unit_price, qty, *args, **kwargs):
    # you would need to do any localization of the result here
    return '{0:.2f}'.format(qty * unit_price)


@register.filter(name='show_entity_image')
def show_entity_image(image, size=None):
    if image:
        if size:
            width, height = size.split('x')
            return image.url + '@{}w_{}h.jpg'.format(width, height)
            # im = get_thumbnail(image.name, size, crop="center")
            # if im:
            #     return im.url
        else:
            return image.url
    return version('images/entity-default.png')


@register.filter(name='show_material_image')
def show_material_image(image):
    if image:
        return image.url
    return version('images/entity-default.png')


@register.filter(name='show_count_down')
def show_count_down(d):
    naive = d.replace(tzinfo=None) + datetime.timedelta(hours=8)
    n = datetime.datetime.now()
    diff = n - naive
    days = diff.days
    minutes, seconds = divmod(diff.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if days <= 0:
        if hours > 0:
            return _('%(hour)d hour ago', '%(hour)d hours ago', hours) % {'hour': hours}
        else:
            if minutes > 0:
                return _('%(minute)d minute ago', '%(minute)d minutes ago', minutes) % {'minute': minutes}
            else:
                return _('%(second)d second ago', '%(second)d seconds ago', minutes) % {'second': seconds}
    else:
        return d.strftime('%Y-%m-%d %H:%M')


@register.filter(name='show_datetime')
def show_datetime(d, delta_hours=0):
    d = d + datetime.timedelta(hours=delta_hours)
    return d.strftime('%Y-%m-%d %H:%M')


@register.filter(name='show_time')
def show_time(d, delta_hours=0):
    d = d + datetime.timedelta(hours=delta_hours)
    return d.strftime('%H:%M')


@register.filter(name='show_date')
def show_date(d):
    if d:
        return d.strftime('%Y-%m-%d')
    return ''


@register.filter(name='show_month')
def show_month(d):
    return d.strftime('%m-%d')


@register.filter(name='show_date')
def show_left_time(d, duration):
    dt = d + datetime.timedelta(hours=duration)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    delta = dt - now
    return ugettext("%.f hour") % (delta.total_seconds() / 3600.0)


@register.filter(name='show_user_title')
def show_user_title(user):
    if user.id == settings.SYSTEM_OPERTOR_ID:
        return settings.SYSTEM_OPERTOR_TITLE
    if user.first_name:
        return user.first_name
    return user.userprofile.cellphone


@register.filter(name='show_head_image')
def show_head_image(user, size='150x150'):
    if hasattr(user, 'userprofile') and user.userprofile:
        if user.userprofile.head_image:
            return show_entity_image(user.userprofile.head_image, size=size)
        elif user.userprofile.gender == codes.Gender.FEMALE.value:
            return "http://pupu.oss-cn-beijing.aliyuncs.com/global_defaultavatar_female.png"
        elif user.userprofile.gender == codes.Gender.MALE.value:
            return "http://pupu.oss-cn-beijing.aliyuncs.com/global_defaultavatar_male.png"
    elif user.id == settings.SYSTEM_OPERTOR_ID:
        return '%simages/logo-wallet.png' % settings.STATIC_URL
    return "http://pupu.oss-cn-beijing.aliyuncs.com/global_defaultavatar_male.png"


@register.filter(name='show_nickname')
def show_nickname(user):
    if user:
        if user.first_name:
            return user.first_name
    return ugettext('unfilled')


@register.filter(name='is_show_upgrade')
def is_show_upgrade(upgrade):
    if upgrade.is_show:
        return ugettext('Yes')
    return ugettext('No')


@register.filter(name='is_force_upgrade')
def is_force_upgrade(upgrade):
    if upgrade.is_force:
        return ugettext('Yes')
    return ugettext('No')


@register.filter(name='show_app_name')
def show_app_name(history_version):
    app_dict = dict((x, y) for x, y in settings.APP_NAME)
    return app_dict[history_version.app_id] if history_version.app_id in app_dict.keys() else u"该产品已经下线"


@register.filter(name='show_app_platform')
def show_app_platform(history_version):
    app_dict = dict((x, y) for x, y in settings.APP_PLATFORM)
    return app_dict[history_version.platform_type] if history_version.platform_type in app_dict.keys() else u"该产品已经下线"


@register.filter(name='show_upgrade_description')
def show_upgrade_description(history_version):
    description = history_version.description
    description = description.replace("\n", "<br/>")
    return mark_safe(description)


@register.filter(name='show_bank_name')
def show_bank_name(bank_type):
    for k, v in settings.BANK_TYPE_LABEL:
        if k == bank_type:
            return v
    return ''


@register.filter(name='show_apply_status')
def show_apply_status(status):
    for k, v in settings.APPLY_STATUS_LABEL:
        if k == status:
            return v
    return ''


@register.filter(name='show_language_icon')
def show_language_icon(request):
    language = translation.get_language()
    for k, v in settings.SUPPORT_LANGUAGES:
        if language == k:
            return language
    return 'en'


@register.filter(name='show_language_code')
def show_language_code(request):
    language = translation.get_language()
    for k, v in settings.SUPPORT_LANGUAGES:
        if language == k:
            return v
    return 'English'


@register.filter(name='is_current_language')
def is_current_language(language_code):
    language = translation.get_language()
    if language_code == language:
        return True
    return False


@register.filter(name='trans_country')
def trans_country(country_code):
    """translate country code to full name
    """
    try:
        return COUNTRIES[country_code]
    except Exception, inst:
        logger.exception(str(inst))
        return ""


@register.filter(name='integer_format')
def integer_format(number):
    """integer format by given parameters
    """
    try:
        output = ''
        cnt = 1
        str_number = str(number)
        length = len(str_number)
        for c in str_number[::-1]:
            output += c
            if cnt % 3 == 0 and cnt != length:
                output += ','
            cnt += 1
        return output[::-1]
    except Exception, inst:
        logger.exception("fail to integer format:%s" % str(inst))
        return ""


class GetCookiesNode(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)

    def render(self, context):
        try:
            cookie_key = self.item.resolve(context)
            logger.info("cookie key is: %s" % cookie_key)
            request = context['request']
            logger.info("value is: %s" % request.COOKIES.get("cookie_key"))
            return request.COOKIES.get("cookie_key")
        except Exception, inst:
            logger.exception("fail to get cookies:%s" % str(inst))
            return ""


@register.tag(name='get_cookie_value')
def get_cookie_value(parser, token):
    """Get cookie value
    """
    return GetCookiesNode(token.split_contents()[1])


def arabic_change_page_style():
    """integer format by given parameters
    """
    try:
        language = translation.get_language()
        if language == 'ar':
            return 'dir="rtl"'
    except Exception, inst:
        logger.exception("fail to arabic_change_page_style:%s" % str(inst))
        return ""


register.simple_tag(arabic_change_page_style)


def arabic_change_style():
    """integer format by given parameters
    """
    try:
        language = translation.get_language()
        if language == 'ar':
            return 'style="text-align:right;"'
    except Exception, inst:
        logger.exception("fail to arabic_change_style:%s" % str(inst))
        return ""


register.simple_tag(arabic_change_style)


def language_change_header_style():
    """integer format by given parameters
    """
    try:
        language = translation.get_language()
        if language in ['de', 'es', 'fr', 'nl', 'ru', 'fi']:
            return 'style="font-size:16px;"'
    except Exception, inst:
        logger.exception("fail to language_change_header_style:%s" % str(inst))
        return ""


register.simple_tag(language_change_header_style)


def russian_change_header_style():
    """integer format by given parameters
    """
    try:
        language = translation.get_language()
        if language == 'ru':
            return 'style="font-size:16px;"'
    except Exception, inst:
        logger.exception("fail to russian_change_header_style:%s" % str(inst))
        return ""


register.simple_tag(russian_change_header_style)


def newpay_page_background_picture():
    """integer format by given parameters
    """
    try:
        language = translation.get_language()
        if language.startswith('zh'):
            return 'newpay_bg_chinese'
        else:
            return 'newpay_bg'
    except Exception, inst:
        logger.exception("fail to newpay page background picture:%s" % str(inst))
        return ""


register.simple_tag(newpay_page_background_picture)
