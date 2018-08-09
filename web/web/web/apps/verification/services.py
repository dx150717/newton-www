#-*- coding: utf-8 -*-
"""Service Implementation of verification module

"""
import logging
import datetime

from django.conf import settings
from django.utils.timezone import utc

from utils import security
from config import codes
from . import models

logger = logging.getLogger(__name__)

def generate_verification_uuid(email, email_type):
    """Generate uuid for verification
    """
    try:
        # genreate uuid
        uuid = security.generate_uuid()
        # save db
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=settings.VERIFICATION_DEFAULT_EXPIRE_TIME)
        verification = models.EmailVerification()
        verification.email_address = email
        verification.uuid = uuid
        verification.email_type = email_type
        verification.expire_time = expire_time
        verification.save()
        # return result
        return verification
    except Exception, inst:
        logger.exception("fail to generate verification uuid:%s" % str(inst))
        return None

def get_verification_by_uuid(uuid, email_type):
    """Get verification by uuid
    """
    try:
        # query
        verification = models.EmailVerification.objects.get(uuid=uuid, email_type=email_type, status=codes.StatusCode.AVAILABLE.value)
        expire_time = verification.expire_time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if now > expire_time:
            logger.info("uuid is expired.")
            return None
        # return result
        return verification
    except Exception, inst:
        logger.exception("fail to get verification by uuid:%s" % str(inst))
        return None
