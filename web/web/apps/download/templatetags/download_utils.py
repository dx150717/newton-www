# -*- coding: utf-8 -*-
import re
import logging
from django import template
from django.template import Context, loader
from django.conf import settings
from django.template import RequestContext
from django.utils import translation

from internal_api_client import internal_api_client

__author__ = 'xiawu@zeuux.org'
__version__ = '$Rev$'
__doc__ = """ """

logger = logging.getLogger(__name__)
register = template.Library()


class DownloadButtonsNode(template.Node): 
    def __init__(self):
        pass
    
    def render(self, context):
        request = context['request']
        print request
        template = loader.get_template('download/include-newpay-download-button.html')
        is_zh = False
        language = str(translation.get_language())
        if language.startswith('zh'):
            is_zh = True
        client = internal_api_client.InternalAPIClient(settings.INTERNAL_API_HOST_IP, settings.INTERNAL_API_HOST_PORT)
        # android
        android_url = ''
        result = None
        try:
            result = client.query_upgrade_data(2, 1).upgrade_data
        except Exception, inst:
            logger.error("fail to query upgrade:%s" % str(inst))
        if result:
            android_url = result[0].download_url
        if not android_url:
            if is_zh:
                android_url = settings.NEWPAY_FOR_ANDROID_ALI_DOWNLOAD_URL
            else:
                android_url = settings.NEWPAY_FOR_ANDROID_ALI_SG_DOWNLOAD_URL
        context = RequestContext(request, locals())
        html = template.render(context)
        return html


@register.tag(name='show_download_buttons')
def show_download_buttons(parser, token):
    return DownloadButtonsNode()
