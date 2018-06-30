# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseForbidden

import decorators
from utils import http
from utils import security
from utils import exception
from tokenexchange import models as tokenexchange_models

logger = logging.getLogger(__name__)

def check_file_permission(request, path):
    """Check the permission of protect file
    """
    try:
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        item = tokenexchange_models.KYCInfo.objects.get(user_id=request.user.id)
        resources = [
            item.id_card, 
            item.personal_profile_attachment, 
            item.your_community_screenshots1,
            item.your_community_screenshots2,
            item.your_community_screenshots3,
            item.done_for_newton_attachment,
            item.orgnization_certificate1,
            item.orgnization_certificate2]
        if path in resources:
            # work around for content type
            content_type = 'image/jpeg'
            if path.endswith('.jpg') or path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif path.endswith('.png'):
                content_type = 'image/png'
            # end
            response = http.HttpResponse()
            response['Content-Type'] = content_type
            response['X-Accel-Redirect'] = '/filestorage/%s' % path
            return response
        else:
            return HttpResponseForbidden()
    except Exception, inst:
        logger.exception("fail to check the file permission:%s" % str(inst))
        return HttpResponseForbidden()
