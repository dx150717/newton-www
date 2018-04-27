"""Service Implementation of verification module

"""
import logging
from datetime import datetime
from datetime import timedelta

from django.conf import settings

from utils import security
from . import models

logger = logging.getLogger(__name__)

def generate_verification_uuid(email, email_type):
    """Generate uuid for verification
    """
    try:
        # genreate uuid
        uuid = security.generate_uuid()
        # save db
        expire_time = datetime.now() + timedelta(seconds=settings.VERIFICATION_DEFAULT_EXPIRE_TIME)
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

def get_verification_by_uuid(uuid):
    """Get verification by uuid
    """
    try:
        # query
        verification = models.EmailVerification.objects.get(uuid=uuid)
        # return result
        return verification
    except Exception, inst:
        return None
