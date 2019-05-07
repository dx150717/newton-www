# -*- coding: utf-8 -*-
import logging
import requests

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation

logger = logging.getLogger(__name__)


def show_newpay_download_view(request):
    is_zh = False
    language = str(translation.get_language())
    if language.startswith('zh'):
        is_zh = True
    code = request.GET.get('code', '')
    if code:
        return render(request, "download/newpay-download-invite.html", locals())
    else:
        return render(request, "download/newpay-download.html", locals())


def show_newpay_guide_view(request):
    is_zh = False
    language = str(translation.get_language())
    if language.startswith('zh'):
        is_zh = True
    return render(request, "download/newpay-guide.html", locals())


def show_newpay_dapp_home_view(request, dapp_id):
    is_zh = False
    language = str(translation.get_language())
    if language.startswith('zh'):
        is_zh = True
    pocket_id = request.GET.get('id')
    pocket_profile = get_dapp_redpocket_profile(pocket_id)
    giver_avatar = ''
    giver_name = ''
    pocket_message = ''

    if pocket_profile:
        giver_avatar = pocket_profile['giver_avatar']
        giver_name = pocket_profile['giver_name']
        pocket_message = pocket_profile['pocket_message']
    redirect_scheme = settings.DAPP_REDPOCKET_SCHEME % pocket_id
    download_url = settings.DAPP_REDPOCKET_DOWNLOAD_URL % pocket_id
    return render(request, "download/newpay-dapp-%s-loading.html" % dapp_id, locals())


def show_newpay_dapp_download_view(request, dapp_id):
    is_zh = False
    language = str(translation.get_language())
    if language.startswith('zh'):
        is_zh = True
    pocket_id = request.GET.get('pocket_id')
    pocket_profile = get_dapp_redpocket_profile(pocket_id)
    giver_avatar = ''
    giver_name = ''
    pocket_message = ''

    if pocket_profile:
        giver_avatar = pocket_profile['giver_avatar']
        giver_name = pocket_profile['giver_name']
        pocket_message = pocket_profile['pocket_message']
            
    download_url = settings.DAPP_REDPOCKET_REDIRECT_URL
    return render(request, "download/newpay-dapp-%s-download.html" % dapp_id, locals())


def  get_dapp_redpocket_profile(pocket_id):
    try:
        response = requests.post(settings.DAPP_REDPOCKET_HEP_API, {'pocket_id':pocket_id})
        result = json.loads(response.content)
        if result['error_code']:
            return result['result']
    except Exception, inst:
        logger.exception("fail to get the redpocket profile:%s" % str(inst))
        return None
