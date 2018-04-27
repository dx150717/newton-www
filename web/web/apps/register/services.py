"""Service Implementation of register module
"""
import logging

from tasks import task_email

logger = logging.getLogger(__name__)


def send_register_validate_email(email):
    try:
        # build the email body
        # send
        task_email.send_email.deplay()
        return True
    except Exception, inst:
        logger.exception("fail to send the register validate email:%s" % str(inst))
        return False
    
