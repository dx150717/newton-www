"""Service Implementation of register module
"""
import logging

from tasks import task_email
from django.conf import settings
from django.template import Template, Context, loader

from verification import service
logger = logging.getLogger(__name__)


def send_register_validate_email():
    try:
        # build the email body
        # send
        subject = "NewtonProject Notifications: Please Register Newton:"
        template = loader.get_template("register/register-letter.html")
        context = Context({"targetUrl":url,"request":request})
        html_content = template.render(context)
        from_email = settings.FROM_EMAIL
        task_email.send_email.delay(subject, html_content, from_email, to_emails)
        return True
    except Exception, inst:
        logger.exception("fail to send the register validate email:%s" % str(inst))
        return False
    
