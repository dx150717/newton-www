"""
Locale Middlwares Implementation includeing POST parameter, HTTP Header, etc.
"""

__copyright__ = """ Copyright (c) 2016 Beijing ShenJiangHuDong Technology Co., Ltd. All rights reserved."""
__version__ = '1.0'
__author__ = 'xiawu@diynova.com'


import logging
from django.utils import translation
from django.middleware import locale
from django.conf import settings

logger = logging.getLogger(__name__)

class LocaleFromPostMiddleware(locale.LocaleMiddleware):
    """
    LocaleFromPostMiddleware: Set the current language code by language filed in POST parameters
    """
    def __get_user_language(self, request):
        try:
            language = request.COOKIES.get('language')
            if not language:
                language = request.META.get('HTTP_ACCEPT_LANGUAGE')
                # Adapt browser language
                if language:
                    language = language.split(',')[0]
            if not language:
                language = request.POST.get("language", None)
            if not language:
                return settings.LANGUAGE_CODE
            if language.find('zh') >= 0:
                return 'zh_CN'
            if language.find('ko') >= 0:
                return 'ko'
            if language.find('ru') >= 0:
                return 'ru'
            if language.find('tr') >= 0:
                return 'tr'
            if language.find('ja') >= 0:
                return 'ja'
            if language.find('es') >= 0:
                return 'es'
            if language.find('fr') >= 0:
                return 'fr'
            if language.find('de') >= 0:
                return 'de'
            if language.find('ar') >= 0:
                return 'ar'
            if language.find('nl') >= 0:
                return 'nl'
            if language.find('fi') >= 0:
                return 'fi'
            if language.find('id') >= 0:
                return 'id'
            if language.find('it') >= 0:
                return 'it'
            if language.find('th') >= 0:
                return 'th'
            if language.find('vi') >= 0:
                return 'vi'
            return 'en'
        except Exception, inst:
            logger.exception('fail to get user language:%s' % str(inst))
            return 'en'

    def process_request(self, request):
        # check the langage in cookie
        language = self.__get_user_language(request)
        if not language:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response
