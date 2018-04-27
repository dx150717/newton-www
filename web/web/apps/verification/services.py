"""Service Implementation of verification module

"""
import logging
import datetime

from utils import security
from . import models

logger = logging.getLogger(__name__)

def generate_verification_uuid(email, email_type):
    """
    """
    try:
        # genreate uuid
        uuid = security.generate_uuid()
        # save db
        verification = models.EmailVerification(email_address=email, uuid=uuid, email_type=email_type, expire_time=datetime.now())
        verification.save()
        # return result
        return verification
    except Exception, inst:
        print(str(inst))
        return None

def get_verification_by_uuid(uuid):
    """
    """
    try:
        # query
        verification = models.EmailVerification.objects.get(uuid=uuid)
        # return result
        return verification
    except Exception, inst:
        return None
