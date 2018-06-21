# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from utils import security
from utils import new_captcha
from utils import http
from ishuman import services as ishuman_services

logger = logging.getLogger(__name__)

def show_captcha_image(request):
    """Show the image content of captcha
    """
    try:
        code = security.generate_uuid()[0:5]
        ishuman_services.set_captcha(request.session.session_key, code)
        return HttpResponse(new_captcha.generate_captcha_image(code), "image/gif")
    except Exception, inst:
        logger.exception("fail to show captcha image:%s" % str(inst))
        return HttpResponse()



def check_captcha(request):
    """Check the captcha
    """
    try:
        code = request.GET.get('code')
        real_code = ishuman_services.get_captcha(request.session.session_key)
        if code and code.lower() == real_code.lower():
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse()
    except Exception, inst:
        logger.exception("fail to check captcha:%s" % str(inst))
        return http.JsonErrorResponse()


