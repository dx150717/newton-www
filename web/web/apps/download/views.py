# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from django.conf import settings
from django.utils import translation

from internal_api_client import internal_api_client

logger = logging.getLogger(__name__)


def show_newpay_download_view(request):
    is_zh = False
    language = str(translation.get_language())
    if language.startswith('zh'):
        is_zh = True
    client = internal_api_client.InternalAPIClient(settings.INTERNAL_API_HOST_IP, settings.INTERNAL_API_HOST_PORT)
    # ios
    ios_url = ''
    result = None
    try:
        result = client.query_upgrade_data(1, 1).upgrade_data
    except Exception, inst:
        logger.error("fail to query upgrade:%s" % str(inst))
    if result:
        ios_url = result[0].download_url
    if not ios_url:
        ios_url = settings.NEWTON_NEWPAY_IOS_URL
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
    code = request.GET.get('code', '')
    if code:
        return render(request, "download/newpay-download-invite.html", locals())
    else:
        return render(request, "download/newpay-download.html", locals())

def show_newpay_guide_view(request):
    return render(request, "download/newpay-guide.html", locals())
